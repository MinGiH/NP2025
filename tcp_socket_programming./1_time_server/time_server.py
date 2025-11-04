#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Time 서버 - TCP/IP 소켓 프로그래밍
현재 시간을 클라이언트에게 전송하는 서버
"""

import socket
import datetime
import sys

def start_time_server(host='0.0.0.0', port=9001):
    """
    Time 서버 시작
    
    Args:
        host: 서버 주소 (0.0.0.0은 모든 네트워크 인터페이스에서 수신)
        port: 포트 번호
    """
    # TCP 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 소켓 재사용 옵션 설정
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # 소켓을 주소와 바인딩
        server_socket.bind((host, port))
        
        # 연결 대기 (최대 5개 대기열)
        server_socket.listen(5)
        
        print("=" * 60)
        print(f"[Time 서버] 서버 시작: {host}:{port}")
        print(f"[Time 서버] 클라이언트 연결 대기 중...")
        print(f"[Time 서버] 종료하려면 Ctrl+C를 누르세요")
        print("=" * 60)
        print()
        
        connection_count = 0
        
        while True:
            # 클라이언트 연결 수락
            client_socket, client_address = server_socket.accept()
            connection_count += 1
            
            print(f"[연결 #{connection_count}] 클라이언트 접속: {client_address[0]}:{client_address[1]}")
            
            try:
                # 현재 시간 가져오기
                current_time = datetime.datetime.now()
                time_str = current_time.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
                
                # 전송할 메시지 생성
                message = f"서버 현재 시간: {time_str}"
                
                # 클라이언트에게 시간 전송
                client_socket.send(message.encode('utf-8'))
                print(f"[전송] {message}")
                
            except Exception as e:
                print(f"[오류] 클라이언트 처리 중 오류 발생: {e}")
            
            finally:
                # 클라이언트 연결 종료
                client_socket.close()
                print(f"[연결 종료] 클라이언트 연결 종료")
                print()
    
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("[Time 서버] 서버를 종료합니다...")
        print(f"[Time 서버] 총 {connection_count}개의 연결을 처리했습니다.")
        print("=" * 60)
    
    except Exception as e:
        print(f"[오류] 서버 오류: {e}")
        sys.exit(1)
    
    finally:
        server_socket.close()
        print("[Time 서버] 서버 소켓 종료 완료")

if __name__ == "__main__":
    # 명령줄 인자에서 포트 번호 가져오기 (기본값: 9001)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9001
    start_time_server(port=port)

