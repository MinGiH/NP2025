# N-Echo TCP/IP 소켓 프로그래밍 프로젝트

객체 지향 이기종 TCP/IP 소켓 프로그래밍 팀 과제

## 📋 프로젝트 개요

이 프로젝트는 TCP/IP 소켓을 사용한 N-Echo 서버/클라이언트 시스템입니다.
- 클라이언트가 서버에 **n**(반복 횟수)과 **message**(메시지)를 전송
- 서버가 메시지를 **n번** 에코하여 응답

## 🏗️ 구성

### 1. Python N-Echo 서버/클라이언트 (과제 1)
- **서버**: `python_server.py` - 객체지향으로 작성된 N-Echo 서버
- **클라이언트**: `python_client.py` - 객체지향으로 작성된 N-Echo 클라이언트
- Windows와 Ubuntu 간 크로스 플랫폼 통신 지원

### 2. Java N-Echo 서버 + Python 클라이언트 (과제 2)
- **서버**: `NEchoServer.java` - Java로 작성된 N-Echo 서버
- **클라이언트**: `python_client.py` - 동일한 Python 클라이언트 사용
- 이기종 언어 간 통신 (Java ↔ Python)

## 📦 파일 구조

```
n-echo-project/
├── python_server.py          # Python N-Echo 서버
├── python_client.py          # Python N-Echo 클라이언트
├── NEchoServer.java          # Java N-Echo 서버
├── setup_java.sh             # Java 설정 스크립트
├── run_java_server.sh        # Java 서버 실행 스크립트
└── README.md                 # 이 파일
```

## 🔧 요구사항

### Python 서버/클라이언트
- Python 3.6 이상
- 기본 라이브러리만 사용 (추가 설치 불필요)

### Java 서버
- JDK 8 이상
- JSON 라이브러리 (org.json)

## 🚀 실행 방법

### 방법 1: Python 서버 + Python 클라이언트

#### 1단계: Python 서버 실행 (서버 측)
```bash
# Ubuntu 또는 Windows에서
python3 python_server.py [포트번호]

# 예시 (기본 포트 5000)
python3 python_server.py

# 예시 (포트 8080 사용)
python3 python_server.py 8080
```

#### 2단계: Python 클라이언트 실행 (클라이언트 측)
```bash
# Ubuntu 또는 Windows에서
python3 python_client.py [서버주소] [포트번호]

# 예시 (로컬호스트, 기본 포트 5000)
python3 python_client.py

# 예시 (원격 서버)
python3 python_client.py 192.168.1.100 5000
```

### 방법 2: Java 서버 + Python 클라이언트

#### 1단계: Java 서버 설정 (최초 1회)
```bash
# Linux/Ubuntu
chmod +x setup_java.sh run_java_server.sh
./setup_java.sh
```

**Windows에서는 수동 설정:**
1. JSON 라이브러리 다운로드:
   ```
   https://repo1.maven.org/maven2/org/json/json/20231013/json-20231013.jar
   ```
2. 컴파일:
   ```cmd
   javac -cp .;json-20231013.jar NEchoServer.java
   ```

#### 2단계: Java 서버 실행 (서버 측)
```bash
# Linux/Ubuntu
./run_java_server.sh [포트번호]

# Windows
java -cp .;json-20231013.jar NEchoServer [포트번호]

# 예시 (기본 포트 5000)
./run_java_server.sh
# 또는
java -cp .;json-20231013.jar NEchoServer
```

#### 3단계: Python 클라이언트 실행 (클라이언트 측)
```bash
# Python 서버와 동일
python3 python_client.py [서버주소] [포트번호]
```

## 💡 사용 예시

### 클라이언트 사용
```
=== N-Echo 클라이언트 ===
종료하려면 'quit' 또는 'exit'를 입력하세요.

에코 횟수 (n): 3
에코할 메시지: Hello, World!
[전송] n=3, message='Hello, World!'

==================================================
[응답 성공]
에코 횟수: 3
에코된 메시지:
  1. Hello, World!
  2. Hello, World!
  3. Hello, World!
==================================================

에코 횟수 (n): quit
클라이언트를 종료합니다.
```

## 🔍 프로토콜 명세

### 요청 형식 (JSON)
```json
{
    "n": 3,
    "message": "Hello, World!"
}
```

### 응답 형식 (JSON)
#### 성공:
```json
{
    "status": "success",
    "n": 3,
    "echoes": ["Hello, World!", "Hello, World!", "Hello, World!"]
}
```

#### 실패:
```json
{
    "status": "error",
    "message": "오류 메시지"
}
```

## 🏛️ 객체지향 설계

### Python 서버 (`python_server.py`)
- **NEchoServer 클래스**
  - `__init__()`: 서버 초기화
  - `start()`: 서버 시작 및 클라이언트 연결 수락
  - `handle_client()`: 클라이언트 요청 처리 (멀티스레딩)
  - `stop()`: 서버 종료

### Python 클라이언트 (`python_client.py`)
- **NEchoClient 클래스**
  - `__init__()`: 클라이언트 초기화
  - `connect()`: 서버 연결
  - `send_request()`: 요청 전송 및 응답 수신
  - `disconnect()`: 연결 종료
  - `display_response()`: 응답 출력

### Java 서버 (`NEchoServer.java`)
- **NEchoServer 클래스**
  - `start()`: 서버 시작 및 클라이언트 연결 수락
  - `stop()`: 서버 종료
  - **ClientHandler 내부 클래스**: 클라이언트 요청 처리 (멀티스레딩)
    - `run()`: 클라이언트 통신 처리
    - `processRequest()`: JSON 요청 파싱 및 응답 생성
    - `createErrorResponse()`: 에러 응답 생성

## 🌐 크로스 플랫폼 지원

- **Windows ↔ Ubuntu**: 완전 호환
- **Python ↔ Java**: JSON 프로토콜을 통한 이기종 통신
- IPv4 지원
- 0.0.0.0 바인딩으로 모든 네트워크 인터페이스에서 접속 가능

## 🔒 주요 기능

1. **멀티 클라이언트 지원**: 여러 클라이언트 동시 접속 가능 (스레드 기반)
2. **에러 처리**: 잘못된 입력 및 연결 오류 처리
3. **유효성 검사**: n은 양의 정수, message는 비어있지 않아야 함
4. **JSON 프로토콜**: 구조화된 데이터 통신
5. **우아한 종료**: Ctrl+C로 안전하게 종료 가능

## 📝 테스트 시나리오

### 시나리오 1: 동일 시스템 테스트
1. 서버 실행 (Python 또는 Java)
2. 같은 컴퓨터에서 클라이언트 실행
3. localhost:5000으로 연결

### 시나리오 2: Windows-Ubuntu 간 통신
1. Ubuntu에서 서버 실행
2. Windows에서 클라이언트 실행 (Ubuntu의 IP 주소 사용)
3. 또는 반대로 실행

### 시나리오 3: Python-Java 이기종 통신
1. Java 서버 실행
2. Python 클라이언트로 연결
3. 정상 동작 확인

## 🐛 문제 해결

### 포트 이미 사용 중
```bash
# 포트를 사용 중인 프로세스 확인
# Linux
sudo lsof -i :5000
# Windows
netstat -ano | findstr :5000

# 다른 포트 사용
python3 python_server.py 8080
```

### 방화벽 문제
- Windows: 방화벽 설정에서 포트 허용
- Ubuntu: `sudo ufw allow 5000/tcp`

### Java 컴파일 오류
- JDK가 설치되어 있는지 확인: `javac -version`
- JSON 라이브러리가 같은 디렉토리에 있는지 확인

## 👥 팀 과제 제출 내용

### 과제 1: Python N-Echo 서버/클라이언트
- ✅ 객체지향 설계
- ✅ TCP/IP 소켓 통신
- ✅ Windows/Ubuntu 크로스 플랫폼 지원
- ✅ n, message 기반 N-Echo 기능

### 과제 2: Java N-Echo 서버
- ✅ Java 객체지향 설계
- ✅ Python 클라이언트와 호환
- ✅ 과제 1과 동일한 기능
- ✅ 이기종 언어 간 통신

## 📚 참고 자료

- Python socket 라이브러리: https://docs.python.org/3/library/socket.html
- Java ServerSocket: https://docs.oracle.com/javase/8/docs/api/java/net/ServerSocket.html
- JSON 라이브러리: https://github.com/stleary/JSON-java

## 📄 라이선스

이 프로젝트는 교육 목적으로 작성되었습니다.

