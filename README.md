# rickandmortyapi-db

[![Python](https://github.com/jinahya/rickandmortyapi-db/actions/workflows/python-app.yml/badge.svg)](https://github.com/jinahya/rickandmortyapi-db/actions/workflows/python-app.yml)

Generates an SQLite database from [The Rick and Morty API](https://rickandmortyapi.com).

See

* [rickandmortyapi-persistence](https://github.com/jinahya/rickandmortyapi-persistence)
* [rickandmortyapi-spring-data-rest](https://github.com/jinahya/rickandmortyapi-spring-data-rest)

## How to

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python3 -m pip install --upgrade pip
$ pip3 install -r requirements.txt
$ python3 rickandmortyapi-db.py
$ ls -l rickandmortyapi.db
$ sqlite3 rickandmortyapi.db ".schema"
```

## Adjustment

### character

* When `$.location.name` is `unknown`, both `location_name` and `location_url` are `NULL`.

## Links

### github.com/afuh/rickandmortyapi

* [#140](https://github.com/afuh/rick-and-morty-api/issues/140) character/125 is not registered as a resident of the
  location/35