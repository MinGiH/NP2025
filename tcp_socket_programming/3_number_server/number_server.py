#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Number 서버 - TCP/IP 소켓 프로그래밍
숫자 맞추기 게임 서버 (1~100 사이의 랜덤 숫자를 맞추는 게임)
"""

import socket
import sys
import random

def handle_client(client_socket, client_address):
    """
    클라이언트와 숫자 맞추기 게임 진행
    
    Args:
        client_socket: 클라이언트 소켓
        client_address: 클라이언트 주소
    """
    # 1~100 사이의 랜덤 숫자 생성
    secret_number = random.randint(1, 100)
    max_attempts = 10
    attempts = 0
    
    print(f"[게임 시작] 정답: {secret_number} (클라이언트에게는 비밀)")
    
    # 환영 메시지 전송
    welcome_msg = (
        "========================================\n"
        "   숫자 맞추기 게임에 오신 것을 환영합니다!\n"
        "========================================\n"
        "규칙:\n"
        "  - 1부터 100 사이의 숫자를 맞춰보세요.\n"
        f"  - 기회는 {max_attempts}번 있습니다.\n"
        "  - 'quit'를 입력하면 포기합니다.\n"
        "========================================\n"
    )
    client_socket.send(welcome_msg.encode('utf-8'))
    
    try:
        while attempts < max_attempts:
            # 클라이언트로부터 숫자 입력 받기
            data = client_socket.recv(1024)
            
            if not data:
                print(f"[알림] 클라이언트가 연결을 종료했습니다.")
                break
            
            user_input = data.decode('utf-8').strip()
            
            # 포기 확인
            if user_input.lower() == 'quit':
                msg = f"\n게임을 포기하셨습니다. 정답은 {secret_number}이었습니다.\n"
                client_socket.send(msg.encode('utf-8'))
                print(f"[알림] 클라이언트가 게임을 포기했습니다.")
                break
            
            # 숫자 유효성 검사
            try:
                guess = int(user_input)
            except ValueError:
                msg = "[오류] 올바른 숫자를 입력해주세요.\n"
                client_socket.send(msg.encode('utf-8'))
                continue
            
            attempts += 1
            remaining = max_attempts - attempts
            
            print(f"[시도 {attempts}] 입력: {guess}")
            
            # 숫자 비교
            if guess < secret_number:
                msg = f"[시도 {attempts}/{max_attempts}] UP! 더 큰 숫자입니다. (남은 기회: {remaining})\n"
                client_socket.send(msg.encode('utf-8'))
                print(f"[응답] UP")
            
            elif guess > secret_number:
                msg = f"[시도 {attempts}/{max_attempts}] DOWN! 더 작은 숫자입니다. (남은 기회: {remaining})\n"
                client_socket.send(msg.encode('utf-8'))
                print(f"[응답] DOWN")
            
            else:
                # 정답!
                msg = (
                    f"\n{'='*40}\n"
                    f"🎉 축하합니다! 정답입니다! 🎉\n"
                    f"정답: {secret_number}\n"
                    f"시도 횟수: {attempts}회\n"
                    f"{'='*40}\n"
                )
                client_socket.send(msg.encode('utf-8'))
                print(f"[게임 종료] 클라이언트가 {attempts}번 만에 정답을 맞췄습니다!")
                break
        
        else:
            # 기회를 모두 사용한 경우
            msg = (
                f"\n{'='*40}\n"
                f"아쉽습니다! 기회를 모두 사용했습니다.\n"
                f"정답은 {secret_number}이었습니다.\n"
                f"{'='*40}\n"
            )
            client_socket.send(msg.encode('utf-8'))
            print(f"[게임 종료] 클라이언트가 기회를 모두 사용했습니다.")
    
    except Exception as e:
        print(f"[오류] 게임 진행 중 오류 발생: {e}")

def start_number_server(host='0.0.0.0', port=9003):
    """
    Number 서버 시작
    
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
        print(f"[Number 서버] 서버 시작: {host}:{port}")
        print(f"[Number 서버] 클라이언트 연결 대기 중...")
        print(f"[Number 서버] 종료하려면 Ctrl+C를 누르세요")
        print("=" * 60)
        print()
        
        game_count = 0
        
        while True:
            # 클라이언트 연결 수락
            client_socket, client_address = server_socket.accept()
            game_count += 1
            
            print(f"[게임 #{game_count}] 클라이언트 접속: {client_address[0]}:{client_address[1]}")
            
            try:
                # 클라이언트와 게임 진행
                handle_client(client_socket, client_address)
                
            except Exception as e:
                print(f"[오류] 클라이언트 처리 중 오류 발생: {e}")
            
            finally:
                # 클라이언트 연결 종료
                client_socket.close()
                print(f"[연결 종료] 클라이언트 연결 종료")
                print()
    
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("[Number 서버] 서버를 종료합니다...")
        print(f"[Number 서버] 총 {game_count}개의 게임을 진행했습니다.")
        print("=" * 60)
    
    except Exception as e:
        print(f"[오류] 서버 오류: {e}")
        sys.exit(1)
    
    finally:
        server_socket.close()
        print("[Number 서버] 서버 소켓 종료 완료")

if __name__ == "__main__":
    # 명령줄 인자에서 포트 번호 가져오기 (기본값: 9003)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9003
    start_number_server(port=port)

