#!/bin/bash
# Java N-Echo 서버 실행 스크립트

PORT=${1:-5000}

echo "=== Java N-Echo 서버 시작 ==="
echo "포트: $PORT"
echo ""

java -cp .:json-20231013.jar NEchoServer $PORT

