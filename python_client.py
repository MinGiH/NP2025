#!/usr/bin/env python3
"""
N-Echo TCP/IP 클라이언트 (Python)
서버에 n과 message를 전송하고 n번 에코된 응답을 받는 클라이언트

이 프로그램은 N-Echo 서버에 연결하여 메시지를 전송하고,
서버로부터 해당 메시지를 n번 반복한 응답을 받는 클라이언트입니다.
"""

# socket: 네트워크 통신을 위한 소켓 라이브러리
import socket
# json: JSON 형식의 데이터를 다루기 위한 라이브러리
import json
# sys: 명령줄 인자 처리를 위한 시스템 라이브러리
import sys


class NEchoClient:
    """
    N-Echo 클라이언트 클래스
    
    이 클래스는 N-Echo 서버와 통신하는 클라이언트의 기능을 담당합니다.
    서버에 연결하고, 요청을 전송하며, 응답을 받아 화면에 표시합니다.
    """
    
    def __init__(self, host='localhost', port=5000):
        """
        클라이언트 초기화 메서드
        
        클라이언트 객체를 생성할 때 서버의 주소와 포트를 설정합니다.
        
        Args:
            host (str): 서버의 IP 주소 또는 호스트명 (기본값: 'localhost')
            port (int): 서버가 열어놓은 포트 번호 (기본값: 5000)
        """
        self.host = host  # 연결할 서버의 주소를 저장
        self.port = port  # 연결할 서버의 포트 번호를 저장
        self.client_socket = None  # 서버와의 연결에 사용할 소켓 객체 (아직 연결 전)
        
    def connect(self):
        """
        서버에 연결하는 메서드
        
        TCP 소켓을 생성하고 서버에 연결을 시도합니다.
        
        Returns:
            bool: 연결 성공 시 True, 실패 시 False
        """
        try:
            # TCP/IP 소켓 생성
            # AF_INET: IPv4 주소 체계 사용
            # SOCK_STREAM: TCP 프로토콜 사용 (안정적인 연결 지향 통신)
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # 서버에 연결 시도
            # (host, port) 튜플 형태로 서버 주소 전달
            self.client_socket.connect((self.host, self.port))
            
            print(f"[연결 성공] 서버 {self.host}:{self.port}에 연결되었습니다.")
            return True
        except Exception as e:
            # 연결 실패 시 에러 메시지 출력
            print(f"[연결 실패] {e}")
            return False
            
    def send_request(self, n, message):
        """
        N-Echo 요청을 서버에 전송하는 메서드
        
        이 메서드는 에코 횟수와 메시지를 JSON 형식으로 만들어 서버에 전송하고,
        서버로부터 받은 응답을 파싱하여 반환합니다.
        
        Args:
            n (int): 메시지를 몇 번 반복할지 (에코 횟수)
            message (str): 에코할 메시지 내용
            
        Returns:
            dict: 서버의 응답을 딕셔너리 형태로 반환 (실패 시 None)
        """
        try:
            # 요청 데이터를 딕셔너리로 생성
            # 서버가 요구하는 형식에 맞춰 'n'과 'message' 키를 포함
            request = {
                'n': n,
                'message': message
            }
            
            # 딕셔너리를 JSON 문자열로 변환 (직렬화)
            # ensure_ascii=False: 한글 등 유니코드 문자를 그대로 유지
            request_data = json.dumps(request, ensure_ascii=False)
            
            # JSON 문자열을 바이트로 인코딩하여 서버에 전송
            # UTF-8 인코딩 사용
            self.client_socket.send(request_data.encode('utf-8'))
            print(f"[전송] n={n}, message='{message}'")
            
            # 서버로부터 응답 수신
            # 최대 4096바이트까지 받음
            response_data = self.client_socket.recv(4096).decode('utf-8')
            
            # 받은 JSON 문자열을 파싱하여 딕셔너리로 변환
            response = json.loads(response_data)
            
            return response
            
        except Exception as e:
            # 오류 발생 시 메시지 출력하고 None 반환
            print(f"[오류] 요청 처리 중 오류: {e}")
            return None
            
    def disconnect(self):
        """
        서버와의 연결을 종료하는 메서드
        
        열려있는 소켓을 닫아 서버와의 연결을 안전하게 종료합니다.
        """
        if self.client_socket:
            # 소켓을 닫아 연결 종료
            self.client_socket.close()
            print("[연결 종료]")
            
    def display_response(self, response):
        """
        서버로부터 받은 응답을 보기 좋게 화면에 출력하는 메서드
        
        응답의 상태에 따라 성공 메시지 또는 에러 메시지를 표시합니다.
        
        Args:
            response (dict): 서버로부터 받은 응답 데이터
        """
        if not response:
            # 응답이 없으면 아무것도 출력하지 않음
            return
            
        # 구분선 출력
        print("\n" + "="*50)
        
        # 응답 상태가 'success'인지 확인
        if response.get('status') == 'success':
            print(f"[응답 성공]")
            print(f"에코 횟수: {response.get('n')}")
            print(f"에코된 메시지:")
            
            # echoes 배열의 각 항목을 번호와 함께 출력
            # enumerate()는 인덱스와 값을 함께 제공 (1부터 시작하도록 설정)
            for i, echo in enumerate(response.get('echoes', []), 1):
                print(f"  {i}. {echo}")
        else:
            # 실패한 경우 에러 메시지 출력
            print(f"[응답 실패] {response.get('message')}")
        
        print("="*50 + "\n")


def main():
    """
    메인 함수 - 프로그램의 진입점
    
    명령줄 인자를 처리하고 클라이언트를 실행합니다.
    사용자로부터 입력을 받아 서버와 통신하는 무한 루프를 실행합니다.
    """
    # 명령줄 인자 처리
    # 첫 번째 인자: 서버 주소 (없으면 기본값 'localhost')
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    # 두 번째 인자: 서버 포트 번호 (없으면 기본값 5000)
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    
    # NEchoClient 객체 생성
    client = NEchoClient(host=host, port=port)
    
    # 서버에 연결 시도
    if not client.connect():
        # 연결 실패 시 프로그램 종료
        return
        
    try:
        # 프로그램 시작 메시지 출력
        print("\n=== N-Echo 클라이언트 ===")
        print("종료하려면 'quit' 또는 'exit'를 입력하세요.\n")
        
        # 메인 루프: 사용자 입력을 계속 받음
        while True:
            # 사용자 입력 처리 블록
            try:
                # 에코 횟수 입력 받기
                n_input = input("에코 횟수 (n): ").strip()
                
                # 종료 명령어 확인
                if n_input.lower() in ['quit', 'exit', 'q']:
                    print("클라이언트를 종료합니다.")
                    break
                
                # 문자열을 정수로 변환
                n = int(n_input)
                
                # 에코 횟수 유효성 검사 (양수여야 함)
                if n <= 0:
                    print("[오류] 에코 횟수는 양의 정수여야 합니다.\n")
                    continue
                
                # 에코할 메시지 입력 받기
                message = input("에코할 메시지: ").strip()
                
                # 메시지가 비어있는지 확인
                if not message:
                    print("[오류] 메시지는 비어있을 수 없습니다.\n")
                    continue
                
                # 서버에 요청 전송하고 응답 받기
                response = client.send_request(n, message)
                
                # 받은 응답을 화면에 출력
                client.display_response(response)
                
            except ValueError:
                # 정수로 변환할 수 없는 입력을 받았을 때
                print("[오류] 에코 횟수는 정수여야 합니다.\n")
            except EOFError:
                # EOF 입력 (Ctrl+D)을 받았을 때
                print("\n클라이언트를 종료합니다.")
                break
                
    except KeyboardInterrupt:
        # Ctrl+C를 눌러 프로그램을 중단했을 때
        print("\n[중단] Ctrl+C 감지")
    finally:
        # 어떤 경우든 종료 시 연결 끊기
        client.disconnect()


# 이 파일이 직접 실행될 때만 main() 함수 호출
# 다른 파일에서 import 될 때는 실행되지 않음
if __name__ == "__main__":
    main()

