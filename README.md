# rickandmortyapi-db

[![Python](https://github.com/jinahya/rickandmortyapi-db/actions/workflows/python-app.yml/badge.svg)](https://github.com/jinahya/rickandmortyapi-db/actions/workflows/python-app.yml)

## Disclaimer

This document was authored with the assistance of Large Language Model (LLM) technology.

이 문서는 대규모 언어 모델(LLM) 기술의 도움을 받아 작성되었습니다.

— Junie

Generates an SQLite database from [The Rick and Morty API](https://rickandmortyapi.com).

See

* [rickandmortyapi-persistence](https://github.com/jinahya/rickandmortyapi-persistence)
* [rickandmortyapi-spring-data-rest](https://github.com/jinahya/rickandmortyapi-spring-data-rest)

## How to

Follow these steps to set up the project and generate the database.

### 1. Set up a Virtual Environment

It is recommended to use a virtual environment to keep the project's dependencies isolated from your system-wide Python.

```shell
# Create a virtual environment named '.venv'
$ python3 -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
$ source .venv/bin/activate
# On Windows:
# $ .venv\Scripts\activate
```

### 2. Install Dependencies

Once the environment is active, install the required libraries.

```shell
$ python3 -m pip install --upgrade pip
$ pip3 install -r requirements.txt
```

### 3. Generate the Database

Run the main script to fetch data from the API and create the SQLite database.

```shell
$ python3 rickandmortyapi-db.py
```

### 4. Verify the Database

You can check if the database file was created and inspect its structure.

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

## Links

### github.com/afuh/rickandmortyapi

* [#140](https://github.com/afuh/rick-and-morty-api/issues/140) character/125 is not registered as a resident of the
  location/35