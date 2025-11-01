#!/usr/bin/env python3
"""
N-Echo TCP/IP 서버 (Python)
클라이언트로부터 n과 message를 받아 message를 n번 응답하는 서버

이 프로그램은 여러 클라이언트의 연결을 동시에 처리할 수 있는 멀티스레드 서버입니다.
각 클라이언트로부터 에코 횟수와 메시지를 받아 해당 메시지를 n번 반복하여 응답합니다.
"""

# socket: 네트워크 통신을 위한 소켓 라이브러리
import socket
# threading: 멀티스레드 처리를 위한 라이브러리 (여러 클라이언트 동시 처리)
import threading
# json: JSON 형식의 데이터를 다루기 위한 라이브러리
import json
# sys: 명령줄 인자 처리를 위한 시스템 라이브러리
import sys


class NEchoServer:
    """
    N-Echo 서버 클래스
    
    이 클래스는 N-Echo 서버의 모든 기능을 담당합니다.
    서버 소켓을 생성하고, 클라이언트 연결을 수락하며,
    각 클라이언트를 별도의 스레드에서 처리합니다.
    """
    
    def __init__(self, host='0.0.0.0', port=5000, max_connections=5):
        """
        서버 초기화 메서드
        
        서버 객체를 생성할 때 필요한 설정을 초기화합니다.
        
        Args:
            host (str): 서버가 바인딩할 주소 (기본값: '0.0.0.0' - 모든 인터페이스)
            port (int): 서버가 사용할 포트 번호 (기본값: 5000)
            max_connections (int): 동시에 대기할 수 있는 최대 연결 수 (기본값: 5)
        """
        self.host = host  # 서버 주소 저장
        self.port = port  # 포트 번호 저장
        self.max_connections = max_connections  # 최대 연결 대기 수 저장
        self.server_socket = None  # 서버 소켓 객체 (아직 생성 전)
        self.running = False  # 서버 실행 상태 플래그
        
    def start(self):
        """
        서버를 시작하는 메서드
        
        서버 소켓을 생성하고, 포트에 바인딩한 후 클라이언트 연결을 수락합니다.
        들어오는 각 클라이언트 연결을 별도의 스레드에서 처리합니다.
        """
        try:
            # TCP/IP 소켓 생성
            # AF_INET: IPv4 주소 체계 사용
            # SOCK_STREAM: TCP 프로토콜 사용 (안정적인 연결 지향 통신)
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # SO_REUSEADDR 옵션 설정
            # 서버 종료 후 즉시 재시작할 수 있도록 포트 재사용 허용
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # 소켓을 특정 주소와 포트에 바인딩
            # (host, port) 튜플 형태로 주소 전달
            self.server_socket.bind((self.host, self.port))
            
            # 연결 대기 시작
            # max_connections: 동시에 대기할 수 있는 최대 연결 요청 수
            self.server_socket.listen(self.max_connections)
            self.running = True  # 서버 실행 상태를 True로 설정
            
            print(f"[서버 시작] {self.host}:{self.port}")
            print(f"[대기 중] 클라이언트 연결을 기다립니다...")
            
            # 메인 루프: 클라이언트 연결 수락
            while self.running:
                try:
                    # 클라이언트 연결 대기 및 수락
                    # accept()는 블로킹 함수로, 연결이 올 때까지 대기
                    # 반환값: (클라이언트 소켓, 클라이언트 주소)
                    client_socket, client_address = self.server_socket.accept()
                    print(f"[연결] 클라이언트 접속: {client_address}")
                    
                    # 새로운 스레드를 생성하여 클라이언트 처리
                    # 이렇게 하면 여러 클라이언트를 동시에 처리할 수 있음
                    client_thread = threading.Thread(
                        target=self.handle_client,  # 실행할 함수
                        args=(client_socket, client_address)  # 함수에 전달할 인자
                    )
                    # daemon=True: 메인 스레드 종료 시 함께 종료
                    client_thread.daemon = True
                    client_thread.start()  # 스레드 시작
                    
                except OSError:
                    # 소켓이 닫혔을 때 발생하는 예외 처리
                    break
                    
        except Exception as e:
            # 서버 시작 중 발생한 예외 처리
            print(f"[오류] 서버 시작 실패: {e}")
        finally:
            # 어떤 경우든 서버 종료 처리
            self.stop()
            
    def handle_client(self, client_socket, client_address):
        """
        개별 클라이언트의 요청을 처리하는 메서드
        
        이 메서드는 별도의 스레드에서 실행되어 한 클라이언트의 모든 요청을 처리합니다.
        클라이언트로부터 데이터를 받아 파싱하고, N-Echo 처리 후 응답을 전송합니다.
        
        Args:
            client_socket: 클라이언트와 통신하는 소켓 객체
            client_address: 클라이언트의 IP 주소와 포트 튜플
        """
        try:
            # 클라이언트가 연결을 유지하는 동안 계속 요청 처리
            while True:
                # 클라이언트로부터 데이터 수신
                # 최대 4096바이트까지 받음
                data = client_socket.recv(4096).decode('utf-8')
                
                # 데이터가 없으면 클라이언트가 연결을 종료한 것
                if not data:
                    print(f"[연결 종료] {client_address}")
                    break
                
                print(f"[수신] {client_address}: {data}")
                
                # JSON 데이터 파싱 및 처리
                try:
                    # JSON 문자열을 딕셔너리로 변환
                    request = json.loads(data)
                    
                    # 요청에서 'n'과 'message' 값 추출
                    # get() 메서드로 안전하게 값 가져오기 (없으면 기본값 사용)
                    n = request.get('n', 1)
                    message = request.get('message', '')
                    
                    # 입력값 유효성 검사
                    # n이 정수이고 양수인지 확인
                    if not isinstance(n, int) or n <= 0:
                        response = {
                            'status': 'error',
                            'message': 'n은 양의 정수여야 합니다.'
                        }
                    # 메시지가 비어있지 않은지 확인
                    elif not message:
                        response = {
                            'status': 'error',
                            'message': 'message는 비어있을 수 없습니다.'
                        }
                    else:
                        # 유효성 검사를 통과하면 N-Echo 응답 생성
                        # 리스트 컴프리헨션으로 메시지를 n번 반복한 배열 생성
                        echoes = [message for _ in range(n)]
                        response = {
                            'status': 'success',
                            'n': n,
                            'echoes': echoes
                        }
                        print(f"[응답] {client_address}에게 메시지를 {n}번 전송")
                        
                except json.JSONDecodeError:
                    # JSON 파싱 실패 시 에러 응답 생성
                    response = {
                        'status': 'error',
                        'message': 'JSON 형식이 올바르지 않습니다.'
                    }
                
                # 응답을 JSON 문자열로 변환
                # ensure_ascii=False: 한글 등 유니코드 문자를 그대로 유지
                response_data = json.dumps(response, ensure_ascii=False)
                
                # UTF-8로 인코딩하여 클라이언트에게 전송
                client_socket.send(response_data.encode('utf-8'))
                
        except Exception as e:
            # 예외 발생 시 에러 메시지 출력
            print(f"[오류] 클라이언트 처리 중 오류 ({client_address}): {e}")
        finally:
            # 모든 경우에 소켓 닫기 (자원 정리)
            client_socket.close()
            print(f"[연결 해제] {client_address}")
            
    def stop(self):
        """
        서버를 종료하는 메서드
        
        서버 실행 플래그를 False로 설정하고 서버 소켓을 닫아
        안전하게 서버를 종료합니다.
        """
        self.running = False  # 서버 실행 플래그를 False로 설정
        if self.server_socket:
            # 서버 소켓이 열려있으면 닫기
            self.server_socket.close()
            print("[서버 종료]")


def main():
    """
    메인 함수 - 프로그램의 진입점
    
    명령줄 인자로 포트 번호를 받아 서버를 생성하고 시작합니다.
    Ctrl+C를 누르면 서버가 안전하게 종료됩니다.
    """
    # 명령줄 인자로 포트 지정 가능
    # 첫 번째 인자: 포트 번호 (없으면 기본값 5000)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    
    # NEchoServer 객체 생성
    # host='0.0.0.0': 모든 네트워크 인터페이스에서 연결 수락
    server = NEchoServer(host='0.0.0.0', port=port)
    
    try:
        # 서버 시작 (블로킹 호출 - 서버가 종료될 때까지 여기서 대기)
        server.start()
    except KeyboardInterrupt:
        # Ctrl+C를 눌러 프로그램을 중단했을 때
        print("\n[중단] Ctrl+C 감지")
        server.stop()


# 이 파일이 직접 실행될 때만 main() 함수 호출
# 다른 파일에서 import 될 때는 실행되지 않음
if __name__ == "__main__":
    main()

