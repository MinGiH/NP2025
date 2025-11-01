#!/bin/bash
# Java N-Echo 서버 설정 스크립트
# JSON 라이브러리 다운로드 및 컴파일

echo "=== Java N-Echo 서버 설정 ==="

# JSON 라이브러리 다운로드
echo "JSON 라이브러리 다운로드 중..."
if [ ! -f "json-20231013.jar" ]; then
    wget https://repo1.maven.org/maven2/org/json/json/20231013/json-20231013.jar
    if [ $? -eq 0 ]; then
        echo "✓ JSON 라이브러리 다운로드 완료"
    else
        echo "✗ JSON 라이브러리 다운로드 실패"
        echo "수동으로 다운로드하세요: https://repo1.maven.org/maven2/org/json/json/20231013/json-20231013.jar"
        exit 1
    fi
else
    echo "✓ JSON 라이브러리가 이미 존재합니다"
fi

# Java 서버 컴파일
echo ""
echo "Java 서버 컴파일 중..."
javac -cp .:json-20231013.jar NEchoServer.java
if [ $? -eq 0 ]; then
    echo "✓ 컴파일 완료"
else
    echo "✗ 컴파일 실패"
    exit 1
fi

echo ""
echo "=== 설정 완료 ==="
echo "서버 실행 방법: ./run_java_server.sh [포트번호]"

