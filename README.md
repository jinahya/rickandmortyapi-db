# rickandmortyapi-db

[![Python](https://github.com/jinahya/rickandmortyapi-db/actions/workflows/python-app.yml/badge.svg)](https://github.com/jinahya/rickandmortyapi-db/actions/workflows/python-app.yml)

Generates an SQLite database from [The Rick and Morty API](https://rickandmortyapi.com).

[The Rick and Morty API](https://rickandmortyapi.com)로부터 SQLite 데이터베이스를 생성합니다.

See

* [rickandmortyapi-persistence](https://github.com/jinahya/rickandmortyapi-persistence)
* [rickandmortyapi-spring-data-rest](https://github.com/jinahya/rickandmortyapi-spring-data-rest)

## Disclaimer

This document was authored with the assistance of Large Language Model (LLM) technology.

이 문서는 대규모 언어 모델(LLM) 기술의 도움을 받아 작성되었습니다.


## How to

Follow these steps to set up the project and generate the database.

데이터베이스를 생성하고 프로젝트를 설정하려면 다음 단계를 따르세요.

### 1. Set up a Virtual Environment / 가상 환경 설정

It is recommended to use a virtual environment to keep the project's dependencies isolated from your system-wide Python.

프로젝트의 의존성을 시스템 전역 Python과 격리하기 위해 가상 환경을 사용하는 것이 권장됩니다.

```shell
# Create a virtual environment named '.venv'
$ python3 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
$ source .venv/bin/activate
# On Windows:
# $ .venv\Scripts\activate
```

### 2. Install Dependencies / 의존성 설치

Once the environment is active, install the required libraries.

환경이 활성화되면 필요한 라이브러리를 설치합니다.

```shell
$ python3 -m pip install --upgrade pip
$ pip3 install -r requirements.txt
```

### 3. Generate the Database / 데이터베이스 생성

Run the main script to fetch data from the API and create the SQLite database.

메인 스크립트를 실행하여 API로부터 데이터를 가져오고 SQLite 데이터베이스를 생성합니다.

```shell
$ python3 rickandmortyapi-db.py
```

### 4. Verify the Database / 데이터베이스 확인

You can check if the database file was created and inspect its structure.

데이터베이스 파일이 생성되었는지 확인하고 그 구조를 검사할 수 있습니다.

```shell
# List files to see 'rickandmortyapi.db'
$ ls -l rickandmortyapi.db

# Inspect the database schema
$ sqlite3 rickandmortyapi.db ".schema"
```

## Adjustment

### character

* When `$.origin.name` is `unknown`, both `origin_name` and `origin_url` are `NULL`.
* When `$.location.name` is `unknown`, both `location_name` and `location_url` are `NULL`.

