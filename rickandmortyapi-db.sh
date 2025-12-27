#!/bin/bash

# Set up a Virtual Environment / 가상 환경 설정
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

# Activate the virtual environment / 가상 환경 활성화
echo "Activating virtual environment..."
source .venv/bin/activate

# Install Dependencies / 의존성 설치
echo "Installing/Updating dependencies..."
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

# Generate the Database / 데이터베이스 생성
echo "Generating the database..."
python3 rickandmortyapi-db.py

# Generate HTML documentation / HTML 문서 생성
echo "Generating HTML documentation..."
python3 -m pydoc -w rickandmortyapi-db

# Update the rickandmortyapi.db.dbhash / 해시 파일 업데이트
echo "Updating hash file..."
if command -v dbhash >/dev/null 2>&1; then
  dbhash rickandmortyapi.db > rickandmortyapi.db.dbhash
else
  echo "Warning: dbhash command not found, skipping hash update."
fi

echo "Done!"
