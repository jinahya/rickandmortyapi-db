# rickandmortyapi-db

Generates an SQLite database from [The Rick and Morty API](https://rickandmortyapi.com).


## How to

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python3 -m pip install --upgrade pip
$ pip3 install -r requirements.txt
$ python3 rickandmortyapi.py
$ ls -l rickandmortyapi.db
$ sqlite3 rickandmortyapi.db ".schema"
```


## Links

### github.com/afuh/rickandmortyapi

* [#140](https://github.com/afuh/rick-and-morty-api/issues/140) character/125 is not registered as a resident of the location/35