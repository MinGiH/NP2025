/**
 * N-Echo TCP/IP 서버 (Java)
 * 클라이언트로부터 n과 message를 받아 message를 n번 응답하는 서버
 * 
 * 이 프로그램은 여러 클라이언트의 연결을 동시에 처리할 수 있는 멀티스레드 서버입니다.
 * 각 클라이언트로부터 에코 횟수와 메시지를 받아 해당 메시지를 n번 반복하여 응답합니다.
 * 
 * 컴파일: javac NEchoServer.java
 * 실행: java NEchoServer [포트번호]
 */

// 입출력 관련 클래스들 (스트림, 리더, 라이터 등)
import java.io.*;
// 네트워크 통신 관련 클래스들 (소켓, 서버소켓 등)
import java.net.*;
// 유틸리티 클래스들 (컬렉션 등)
import java.util.*;
// JSON 처리를 위한 라이브러리
import org.json.*;

/**
 * N-Echo 서버 메인 클래스
 * 
 * 이 클래스는 N-Echo 서버의 모든 기능을 담당합니다.
 * 서버 소켓을 생성하고, 클라이언트 연결을 수락하며,
 * 각 클라이언트를 별도의 스레드에서 처리합니다.
 */
public class NEchoServer {
    // 서버가 바인딩할 주소 (0.0.0.0은 모든 네트워크 인터페이스)
    private String host;
    // 서버가 사용할 포트 번호
    private int port;
    // 동시에 대기할 수 있는 최대 연결 수
    private int maxConnections;
    // 서버 소켓 객체
    private ServerSocket serverSocket;
    // 서버 실행 상태 플래그
    private boolean running;
    
    /**
     * 서버 생성자
     * 
     * 서버 객체를 생성할 때 필요한 설정을 초기화합니다.
     * 
     * @param host 서버가 바인딩할 주소 (예: "0.0.0.0")
     * @param port 서버가 사용할 포트 번호 (예: 5000)
     * @param maxConnections 동시에 대기할 수 있는 최대 연결 수 (예: 5)
     */
    public NEchoServer(String host, int port, int maxConnections) {
        this.host = host;  // 서버 주소 저장
        this.port = port;  // 포트 번호 저장
        this.maxConnections = maxConnections;  // 최대 연결 대기 수 저장
        this.running = false;  // 초기에는 서버가 실행 중이 아님
    }
    
    /**
     * 서버를 시작하는 메서드
     * 
     * 서버 소켓을 생성하고, 포트에 바인딩한 후 클라이언트 연결을 수락합니다.
     * 들어오는 각 클라이언트 연결을 별도의 스레드에서 처리합니다.
     */
    public void start() {
        try {
            // 서버 소켓 생성 및 특정 주소/포트에 바인딩
            if (host.equals("0.0.0.0")) {
                // 모든 네트워크 인터페이스에서 연결 수락
                serverSocket = new ServerSocket(port, maxConnections);
            } else {
                // 특정 주소에만 바인딩
                InetAddress addr = InetAddress.getByName(host);
                serverSocket = new ServerSocket(port, maxConnections, addr);
            }
            
            // SO_REUSEADDR 옵션 설정
            // 서버 종료 후 즉시 재시작할 수 있도록 포트 재사용 허용
            serverSocket.setReuseAddress(true);
            running = true;  // 서버 실행 상태를 true로 설정
            
            System.out.println("[서버 시작] " + host + ":" + port);
            System.out.println("[대기 중] 클라이언트 연결을 기다립니다...");
            
            // 메인 루프: 클라이언트 연결 수락
            while (running) {
                try {
                    // 클라이언트 연결 대기 및 수락
                    // accept()는 블로킹 메서드로, 연결이 올 때까지 대기
                    Socket clientSocket = serverSocket.accept();
                    
                    // 연결된 클라이언트의 정보 추출
                    InetAddress clientAddress = clientSocket.getInetAddress();
                    int clientPort = clientSocket.getPort();
                    
                    System.out.println("[연결] 클라이언트 접속: " + 
                                     clientAddress + ":" + clientPort);
                    
                    // 새로운 스레드를 생성하여 클라이언트 처리
                    // 이렇게 하면 여러 클라이언트를 동시에 처리할 수 있음
                    ClientHandler handler = new ClientHandler(clientSocket);
                    Thread thread = new Thread(handler);
                    
                    // daemon 스레드로 설정: 메인 스레드 종료 시 함께 종료
                    thread.setDaemon(true);
                    thread.start();  // 스레드 시작
                    
                } catch (SocketException e) {
                    // 소켓이 닫혔을 때 발생하는 예외 처리
                    if (!running) {
                        break;  // 의도적인 종료인 경우 루프 탈출
                    }
                    throw e;  // 그 외의 경우 예외 던지기
                }
            }
            
        } catch (Exception e) {
            // 서버 시작 중 발생한 예외 처리
            System.err.println("[오류] 서버 시작 실패: " + e.getMessage());
            e.printStackTrace();  // 상세한 에러 정보 출력
        } finally {
            // 어떤 경우든 서버 종료 처리
            stop();
        }
    }
    
    /**
     * 서버를 종료하는 메서드
     * 
     * 서버 실행 플래그를 false로 설정하고 서버 소켓을 닫아
     * 안전하게 서버를 종료합니다.
     */
    public void stop() {
        running = false;  // 서버 실행 플래그를 false로 설정
        try {
            // 서버 소켓이 null이 아니고 닫혀있지 않으면 닫기
            if (serverSocket != null && !serverSocket.isClosed()) {
                serverSocket.close();
            }
            System.out.println("[서버 종료]");
        } catch (IOException e) {
            // 서버 종료 중 발생한 예외 처리
            System.err.println("[오류] 서버 종료 중 오류: " + e.getMessage());
        }
    }
    
    /**
     * 클라이언트 처리 핸들러 내부 클래스
     * 
     * 이 클래스는 개별 클라이언트와의 통신을 담당합니다.
     * Runnable 인터페이스를 구현하여 별도의 스레드에서 실행됩니다.
     */
    class ClientHandler implements Runnable {
        // 클라이언트와 통신하는 소켓
        private Socket clientSocket;
        // 클라이언트 주소 정보 (로그 출력용)
        private String clientAddress;
        
        /**
         * ClientHandler 생성자
         * 
         * @param socket 클라이언트와 연결된 소켓 객체
         */
        public ClientHandler(Socket socket) {
            this.clientSocket = socket;
            // 클라이언트 주소를 문자열로 저장 (IP:Port 형식)
            this.clientAddress = socket.getInetAddress() + ":" + socket.getPort();
        }
        
        /**
         * 스레드 실행 메서드 (Runnable 인터페이스 구현)
         * 
         * 이 메서드는 스레드가 시작될 때 자동으로 호출됩니다.
         * 클라이언트로부터 데이터를 읽고, 처리하고, 응답을 전송합니다.
         */
        @Override
        public void run() {
            // try-with-resources: 자동으로 리소스를 닫아줌
            try (
                // 클라이언트로부터 데이터를 읽기 위한 BufferedReader
                // UTF-8 인코딩으로 텍스트 데이터 읽기
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(clientSocket.getInputStream(), "UTF-8"));
                // 클라이언트에게 데이터를 쓰기 위한 PrintWriter
                // 두 번째 파라미터 true: 자동 flush (즉시 전송)
                PrintWriter out = new PrintWriter(
                    new OutputStreamWriter(clientSocket.getOutputStream(), "UTF-8"), true)
            ) {
                String line;
                // 클라이언트가 보낸 각 줄을 읽음 (null이면 연결 종료)
                while ((line = in.readLine()) != null) {
                    System.out.println("[수신] " + clientAddress + ": " + line);
                    
                    // 받은 요청 데이터를 처리하여 응답 생성
                    String response = processRequest(line);
                    
                    // 응답을 클라이언트에게 전송
                    // println()은 줄바꿈 문자를 자동으로 추가
                    out.println(response);
                }
                
                System.out.println("[연결 종료] " + clientAddress);
                
            } catch (Exception e) {
                // 예외 발생 시 에러 메시지 출력
                System.err.println("[오류] 클라이언트 처리 중 오류 (" + 
                                 clientAddress + "): " + e.getMessage());
            } finally {
                // 모든 경우에 소켓 닫기 (자원 정리)
                try {
                    clientSocket.close();
                    System.out.println("[연결 해제] " + clientAddress);
                } catch (IOException e) {
                    System.err.println("[오류] 소켓 종료 실패: " + e.getMessage());
                }
            }
        }
        
        /**
         * 클라이언트 요청을 처리하는 메서드
         * 
         * JSON 형식의 요청 데이터를 파싱하고, 유효성을 검사한 후
         * N-Echo 응답을 생성하여 JSON 문자열로 반환합니다.
         * 
         * @param requestData JSON 형식의 요청 데이터 문자열
         * @return JSON 형식의 응답 데이터 문자열
         */
        private String processRequest(String requestData) {
            try {
                // JSON 문자열을 JSONObject로 파싱
                JSONObject request = new JSONObject(requestData);
                
                // 필수 파라미터 존재 여부 확인
                // 'n'과 'message' 키가 모두 있어야 함
                if (!request.has("n") || !request.has("message")) {
                    return createErrorResponse("n과 message는 필수 파라미터입니다.");
                }
                
                // 파라미터 값 추출
                int n = request.getInt("n");  // 에코 횟수
                String message = request.getString("message");  // 에코할 메시지
                
                // 에코 횟수 유효성 검사 (양수여야 함)
                if (n <= 0) {
                    return createErrorResponse("n은 양의 정수여야 합니다.");
                }
                
                // 메시지가 비어있는지 확인
                if (message == null || message.isEmpty()) {
                    return createErrorResponse("message는 비어있을 수 없습니다.");
                }
                
                // 유효성 검사를 통과하면 N-Echo 응답 생성
                JSONObject response = new JSONObject();
                response.put("status", "success");  // 성공 상태
                response.put("n", n);  // 에코 횟수
                
                // 메시지를 n번 반복한 배열 생성
                JSONArray echoes = new JSONArray();
                for (int i = 0; i < n; i++) {
                    echoes.put(message);  // 배열에 메시지 추가
                }
                response.put("echoes", echoes);  // 응답에 배열 추가
                
                System.out.println("[응답] " + clientAddress + 
                                 "에게 메시지를 " + n + "번 전송");
                
                // JSONObject를 문자열로 변환하여 반환
                return response.toString();
                
            } catch (JSONException e) {
                // JSON 파싱 실패 시 에러 응답 반환
                return createErrorResponse("JSON 형식이 올바르지 않습니다: " + 
                                         e.getMessage());
            } catch (Exception e) {
                // 기타 예외 발생 시 에러 응답 반환
                return createErrorResponse("요청 처리 중 오류: " + e.getMessage());
            }
        }
        
        /**
         * 에러 응답을 생성하는 헬퍼 메서드
         * 
         * 에러 상태와 메시지를 포함하는 JSON 응답을 생성합니다.
         * 
         * @param errorMessage 클라이언트에게 전달할 에러 메시지
         * @return JSON 형식의 에러 응답 문자열
         */
        private String createErrorResponse(String errorMessage) {
            // 에러 응답 JSON 객체 생성
            JSONObject response = new JSONObject();
            response.put("status", "error");  // 실패 상태
            response.put("message", errorMessage);  // 에러 메시지
            // JSON을 문자열로 변환하여 반환
            return response.toString();
        }
    }
    
    /**
     * 메인 함수 - 프로그램의 진입점
     * 
     * 명령줄 인자를 처리하고 서버를 생성하여 시작합니다.
     * Ctrl+C를 누르면 서버가 안전하게 종료됩니다.
     * 
     * @param args 명령줄 인자 배열 (첫 번째 인자: 포트번호)
     */
    public static void main(String[] args) {
        // 기본 포트 번호 설정
        int port = 5000;
        
        // 명령줄 인자로 포트 지정 가능
        if (args.length > 0) {
            try {
                // 첫 번째 인자를 정수로 파싱
                port = Integer.parseInt(args[0]);
            } catch (NumberFormatException e) {
                // 숫자가 아닌 값이 입력된 경우
                System.err.println("[오류] 올바른 포트 번호를 입력하세요.");
                System.exit(1);  // 프로그램 종료
            }
        }
        
        // NEchoServer 객체 생성
        // host: "0.0.0.0" (모든 네트워크 인터페이스)
        // port: 명령줄 인자 또는 기본값 5000
        // maxConnections: 5 (최대 5개 연결 대기)
        NEchoServer server = new NEchoServer("0.0.0.0", port, 5);
        
        // Ctrl+C 처리를 위한 셧다운 훅 등록
        // JVM 종료 시 자동으로 실행될 코드 지정
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("\n[중단] 서버를 종료합니다...");
            server.stop();  // 서버 안전하게 종료
        }));
        
        // 서버 시작 (블로킹 호출 - 서버가 종료될 때까지 여기서 대기)
        server.start();
    }
}

