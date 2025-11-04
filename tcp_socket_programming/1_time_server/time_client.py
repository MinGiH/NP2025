#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Time 클라이언트 - TCP/IP 소켓 프로그래밍
Time 서버에 접속하여 현재 시간을 받아오는 클라이언트
"""

import socket
import sys

def connect_time_server(host='127.0.0.1', port=9001):
    """
    Time 서버에 접속하여 시간 받아오기
    
    Args:
        host: 서버 주소
        port: 서버 포트 번호
    """
    # TCP 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print("=" * 60)
        print(f"[Time 클라이언트] 서버에 연결 시도: {host}:{port}")
        print("=" * 60)
        
        # 서버에 연결
        client_socket.connect((host, port))
        print(f"[연결 성공] 서버에 연결되었습니다.")
        print()
        
        # 서버로부터 데이터 수신 (최대 1024 바이트)
        data = client_socket.recv(1024)
        
        if data:
            message = data.decode('utf-8')
            print(f"[수신 메시지]")
            print(f"  {message}")
            print()
        else:
            print("[경고] 서버로부터 데이터를 받지 못했습니다.")
        
        print("=" * 60)
        print("[Time 클라이언트] 연결 종료")
        print("=" * 60)
        
    except ConnectionRefusedError:
        print(f"[오류] 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        print(f"       주소: {host}:{port}")
    
    except Exception as e:
        print(f"[오류] 클라이언트 오류: {e}")
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    # 명령줄 인자 처리
    if len(sys.argv) >= 2:
        host = sys.argv[1]
        port = int(sys.argv[2]) if len(sys.argv) >= 3 else 9001
    else:
        host = '127.0.0.1'
        port = 9001
    
    connect_time_server(host, port)

