# TCP/IP 소켓 프로그래밍 과제

## 📋 과제 내용
Windows와 Ubuntu Linux 간 TCP/IP 소켓 통신을 구현한 3가지 서버-클라이언트 프로그램

---

## 🗂️ 프로젝트 구조

```
tcp_socket_programming/
├── 1_time_server/
│   ├── time_server.py    # Time 서버
│   └── time_client.py    # Time 클라이언트
├── 2_echo_server/
│   ├── echo_server.py    # Echo 서버
│   └── echo_client.py    # Echo 클라이언트
├── 3_number_server/
│   ├── number_server.py  # Number 게임 서버
│   └── number_client.py  # Number 게임 클라이언트
└── README.md
```

---

## 📦 요구사항

### 필수 소프트웨어
- Python 3.6 이상
- Windows 또는 Linux 운영체제
- 네트워크 연결

### 포트 사용
- Time 서버: **9001**번 포트
- Echo 서버: **9002**번 포트
- Number 서버: **9003**번 포트

---

## 🚀 실행 방법

### 1️⃣ Time 서버 (현재 시간 전송)

**서버 실행 (Ubuntu Linux):**
```bash
cd tcp_socket_programming/1_time_server
python3 time_server.py
# 또는 포트 지정: python3 time_server.py 9001
```

**클라이언트 실행 (Windows):**
```cmd
cd tcp_socket_programming\1_time_server
python time_client.py <서버_IP_주소>
# 예: python time_client.py 192.168.1.100
```

**동작 설명:**
- 클라이언트가 서버에 접속하면 서버의 현재 시간을 받아옴
- 한 번 접속 후 자동 종료

---

### 2️⃣ Echo 서버 (메시지 에코)

**서버 실행 (Ubuntu Linux):**
```bash
cd tcp_socket_programming/2_echo_server
python3 echo_server.py
# 또는 포트 지정: python3 echo_server.py 9002
```

**클라이언트 실행 (Windows):**
```cmd
cd tcp_socket_programming\2_echo_server
python echo_client.py <서버_IP_주소>
# 예: python echo_client.py 192.168.1.100
```

**동작 설명:**
- 클라이언트가 메시지를 입력하면 서버가 그대로 돌려줌
- 여러 메시지를 주고받을 수 있음
- `quit` 또는 `exit` 입력 시 종료

---

### 3️⃣ Number 서버 (숫자 맞추기 게임)

**서버 실행 (Ubuntu Linux):**
```bash
cd tcp_socket_programming/3_number_server
python3 number_server.py
# 또는 포트 지정: python3 number_server.py 9003
```

**클라이언트 실행 (Windows):**
```cmd
cd tcp_socket_programming\3_number_server
python number_client.py <서버_IP_주소>
# 예: python number_client.py 192.168.1.100
```

**게임 규칙:**
- 서버가 1~100 사이의 랜덤 숫자를 생성
- 클라이언트는 10번의 기회 안에 숫자를 맞춰야 함
- UP/DOWN 힌트 제공
- `quit` 입력 시 포기 가능

---

## 🔧 Linux에서 서버 IP 주소 확인 방법

```bash
# 방법 1: ifconfig 사용
ifconfig

# 방법 2: ip addr 사용
ip addr show

# 방법 3: hostname 사용
hostname -I
```

---

## 🧪 테스트 시나리오

### 시나리오 1: Linux 서버 + Windows 클라이언트

1. **Ubuntu Linux (서버):**
   ```bash
   # 서버 IP 확인
   hostname -I
   # 예: 192.168.1.100
   
   # Time 서버 실행
   python3 1_time_server/time_server.py
   ```

2. **Windows (클라이언트):**
   ```cmd
   # Time 클라이언트 실행
   python 1_time_server\time_client.py 192.168.1.100
   ```

### 시나리오 2: Windows 서버 + Linux 클라이언트

1. **Windows (서버):**
   ```cmd
   # 서버 IP 확인
   ipconfig
   # 예: 192.168.1.200
   
   # Echo 서버 실행
   python 2_echo_server\echo_server.py
   ```

2. **Ubuntu Linux (클라이언트):**
   ```bash
   # Echo 클라이언트 실행
   python3 2_echo_server/echo_client.py 192.168.1.200
   ```

### 로컬 테스트 (같은 컴퓨터)

서버와 클라이언트를 같은 컴퓨터에서 테스트하려면:

**터미널 1 (서버):**
```bash
python3 1_time_server/time_server.py
```

**터미널 2 (클라이언트):**
```bash
python3 1_time_server/time_client.py 127.0.0.1
# 또는 그냥
python3 1_time_server/time_client.py
```

---

## 🔥 방화벽 설정

### Ubuntu Linux (서버)
```bash
# 포트 열기
sudo ufw allow 9001/tcp
sudo ufw allow 9002/tcp
sudo ufw allow 9003/tcp

# 방화벽 상태 확인
sudo ufw status
```

### Windows (서버)
Windows 방화벽에서 인바운드 규칙 추가:
- 포트 9001, 9002, 9003 TCP 허용

---

## 📊 프로그램 특징

### 1. Time 서버
- **프로토콜:** TCP
- **기능:** 서버의 현재 시간을 클라이언트에게 전송
- **사용 사례:** 시간 동기화, 기본 소켓 통신 학습

### 2. Echo 서버
- **프로토콜:** TCP
- **기능:** 클라이언트가 보낸 메시지를 그대로 반환
- **사용 사례:** 네트워크 테스트, 양방향 통신 학습

### 3. Number 서버
- **프로토콜:** TCP
- **기능:** 숫자 맞추기 게임 (1~100)
- **사용 사례:** 상태 유지 통신, 게임 로직 구현

---

## 🐛 문제 해결

### 문제: "Address already in use" 오류
**원인:** 포트가 이미 사용 중
**해결:**
```bash
# Linux에서 포트 사용 프로세스 확인 및 종료
sudo lsof -i :9001
sudo kill -9 <PID>

# 또는 다른 포트 사용
python3 time_server.py 9999
```

### 문제: "Connection refused" 오류
**원인:** 서버가 실행되지 않았거나 방화벽 차단
**해결:**
1. 서버가 실행 중인지 확인
2. IP 주소가 올바른지 확인
3. 방화벽 설정 확인

### 문제: Windows에서 Python 명령어 오류
**해결:**
- `python` 대신 `python3` 시도
- 또는 `py` 명령어 사용

---

## 💡 핵심 개념

### TCP/IP 소켓 프로그래밍
- **TCP (Transmission Control Protocol):** 신뢰성 있는 연결 지향 프로토콜
- **소켓 (Socket):** 네트워크 통신의 끝점 (endpoint)
- **서버 (Server):** 요청을 기다리고 처리하는 프로그램
- **클라이언트 (Client):** 서버에 요청을 보내는 프로그램

### 주요 소켓 함수
```python
# 서버
socket()        # 소켓 생성
bind()          # 주소 바인딩
listen()        # 연결 대기
accept()        # 연결 수락
send()/recv()   # 데이터 송수신
close()         # 연결 종료

# 클라이언트
socket()        # 소켓 생성
connect()       # 서버 연결
send()/recv()   # 데이터 송수신
close()         # 연결 종료
```

---

## 📝 과제 제출 시 포함 내용

1. ✅ **소스 코드** (6개 파일)
   - time_server.py, time_client.py
   - echo_server.py, echo_client.py
   - number_server.py, number_client.py

2. ✅ **실행 결과 스크린샷**
   - 각 서버/클라이언트 실행 화면
   - Windows ↔ Linux 간 통신 화면

3. ✅ **보고서**
   - 프로그램 설명
   - 실행 방법
   - 테스트 결과
   - 소스 코드 설명

---

## 👤 작성자 정보

- **과제명:** TCP/IP 소켓 프로그래밍 (10~11장 개인 과제)
- **작성일:** 2025년 11월 3일
- **환경:** Windows 클라이언트 ↔ Ubuntu Linux 서버

---

## 📚 참고 자료

- Python Socket Programming Documentation
- TCP/IP Protocol Suite
- Computer Networking: A Top-Down Approach

---

## ⚖️ 라이센스

이 프로젝트는 교육 목적으로 작성되었습니다.

