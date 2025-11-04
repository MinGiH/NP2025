#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo 클라이언트 - TCP/IP 소켓 프로그래밍
Echo 서버에 접속하여 메시지를 보내고 응답을 받는 클라이언트
"""

import socket
import sys

def connect_echo_server(host='127.0.0.1', port=9002):
    """
    Echo 서버에 접속하여 메시지 주고받기
    
    Args:
        host: 서버 주소
        port: 서버 포트 번호
    """
    # TCP 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print("=" * 60)
        print(f"[Echo 클라이언트] 서버에 연결 시도: {host}:{port}")
        print("=" * 60)
        
        # 서버에 연결
        client_socket.connect((host, port))
        print(f"[연결 성공] 서버에 연결되었습니다.")
        print()
        print("사용법:")
        print("  - 메시지를 입력하면 서버가 그대로 돌려줍니다.")
        print("  - 'quit' 또는 'exit'를 입력하면 종료합니다.")
        print("=" * 60)
        print()
        
        message_count = 0
        
        while True:
            # 사용자로부터 메시지 입력받기
            message = input("[입력] 메시지를 입력하세요: ")
            
            if not message:
                print("[경고] 빈 메시지는 전송할 수 없습니다.")
                continue
            
            message_count += 1
            
            # 서버에 메시지 전송
            client_socket.send(message.encode('utf-8'))
            print(f"[전송 #{message_count}] {message}")
            
            # 서버로부터 응답 수신
            data = client_socket.recv(1024)
            
            if data:
                response = data.decode('utf-8')
                print(f"[수신 #{message_count}] {response}")
                print()
            else:
                print("[경고] 서버로부터 응답을 받지 못했습니다.")
                break
            
            # 종료 명령 확인
            if message.lower().strip() in ['quit', 'exit']:
                break
        
        print("=" * 60)
        print(f"[Echo 클라이언트] 총 {message_count}개의 메시지를 전송했습니다.")
        print("[Echo 클라이언트] 연결 종료")
        print("=" * 60)
        
    except ConnectionRefusedError:
        print(f"[오류] 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        print(f"       주소: {host}:{port}")
    
    except KeyboardInterrupt:
        print("\n[알림] 사용자가 연결을 종료했습니다.")
    
    except Exception as e:
        print(f"[오류] 클라이언트 오류: {e}")
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    # 명령줄 인자 처리
    if len(sys.argv) >= 2:
        host = sys.argv[1]
        port = int(sys.argv[2]) if len(sys.argv) >= 3 else 9002
    else:
        host = '127.0.0.1'
        port = 9002
    
    connect_echo_server(host, port)

