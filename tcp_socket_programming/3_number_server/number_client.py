#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Number 클라이언트 - TCP/IP 소켓 프로그래밍
Number 서버에 접속하여 숫자 맞추기 게임을 플레이하는 클라이언트
"""

import socket
import sys

def connect_number_server(host='127.0.0.1', port=9003):
    """
    Number 서버에 접속하여 숫자 맞추기 게임 플레이
    
    Args:
        host: 서버 주소
        port: 서버 포트 번호
    """
    # TCP 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print("=" * 60)
        print(f"[Number 클라이언트] 서버에 연결 시도: {host}:{port}")
        print("=" * 60)
        
        # 서버에 연결
        client_socket.connect((host, port))
        print(f"[연결 성공] 서버에 연결되었습니다.")
        print()
        
        # 환영 메시지 수신
        welcome_data = client_socket.recv(2048)
        if welcome_data:
            print(welcome_data.decode('utf-8'))
        
        # 게임 진행
        while True:
            # 사용자로부터 숫자 입력받기
            user_input = input("[입력] 숫자를 입력하세요 (1-100, quit=포기): ")
            
            if not user_input:
                print("[경고] 입력이 비어있습니다.")
                continue
            
            # 서버에 입력 전송
            client_socket.send(user_input.encode('utf-8'))
            
            # 서버로부터 응답 수신
            data = client_socket.recv(2048)
            
            if not data:
                print("[알림] 서버와의 연결이 종료되었습니다.")
                break
            
            response = data.decode('utf-8')
            print(response)
            
            # 게임 종료 조건 확인
            if "축하합니다" in response or "아쉽습니다" in response or "포기" in response:
                break
        
        print("=" * 60)
        print("[Number 클라이언트] 게임 종료")
        print("=" * 60)
        
    except ConnectionRefusedError:
        print(f"[오류] 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        print(f"       주소: {host}:{port}")
    
    except KeyboardInterrupt:
        print("\n[알림] 사용자가 게임을 종료했습니다.")
    
    except Exception as e:
        print(f"[오류] 클라이언트 오류: {e}")
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    # 명령줄 인자 처리
    if len(sys.argv) >= 2:
        host = sys.argv[1]
        port = int(sys.argv[2]) if len(sys.argv) >= 3 else 9003
    else:
        host = '127.0.0.1'
        port = 9003
    
    connect_number_server(host, port)

