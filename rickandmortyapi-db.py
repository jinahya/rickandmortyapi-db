import argparse
import datetime
import os
import requests
import sqlite3
from typing import Callable, Any

# ----------------------------------------------------------------------------------------------------------------------
args = None
db_file = "rickandmortyapi.db"


def connect(operation: Callable[[sqlite3.Connection], Any]) -> Any:
    """
    Manages the lifecycle of a database connection and executes a given operation.
    데이터베이스 연결의 수명 주기를 관리하고 지정된 작업을 실행합니다.

    :param operation: A callable that takes a sqlite3.Connection and returns Any.
                      sqlite3.Connection을 인자로 받고 Any를 반환하는 콜러블.
    :return: The result of the operation. 작업의 결과.
    """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        if args and args.debug:
            connection.set_trace_callback(lambda s: print(f"Executing SQL statement: {s}"))
        connection.execute("PRAGMA foreign_keys=ON")
        result = operation(connection)
        return result
    except sqlite3.Error as e:
        print(f"database error: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            connection.close()


def create():
    """
    Creates a new database by executing the DDL script.
    DDL 스크립트를 실행하여 새 데이터베이스를 생성합니다.
    """
    # remove existing database file
    if os.path.exists(db_file):
        print(f"removing existing database file: '{db_file}'")
        os.remove(db_file)
    # open the DDL script
    sql_file = "rickandmortyapi-db.sql"
    try:
        with open(sql_file, "r", encoding="utf-8") as f:
            sql_script = f.read()
        # execute the DDL script
        connection = None
        try:
            connection = sqlite3.connect(db_file)
            if args and args.debug:
                connection.set_trace_callback(lambda s: print(f"Executing SQL statement: {s}"))
            connection.execute("PRAGMA foreign_keys=ON")
            cursor = connection.cursor()
            print(f"new database '{db_file}' created and connected")
            cursor.executescript(sql_script)
            connection.commit()
            print(f"successfully executed DDL script from '{sql_file}'")
        except sqlite3.Error as e:
            print(f"a database error occurred: {e}")
        finally:
            if connection:
                connection.close()
    except IOError as e:
        print(f"an error reading the SQL file occurred: {e}")


base_url = "https://rickandmortyapi.com/api"


def read(path, page=1):
    """
    Fetches data from the Rick and Morty API for a given path and page.
    지정된 경로와 페이지에 대해 Rick and Morty API에서 데이터를 가져옵니다.

    :param path: The API endpoint path (e.g., "/location"). API 엔드포인트 경로 (예: "/location").
    :param page: The page number to fetch. 가져올 페이지 번호.
    :return: The JSON response as a dictionary, or None if not found or an error occurred.
             딕셔너리 형태의 JSON 응답, 또는 찾지 못했거나 오류가 발생한 경우 None.
    """
    full_url = f"{base_url}{path}?page={page}"
    try:
        response = requests.get(full_url)
        if response.status_code == requests.codes.not_found:
            return None
        # response.raise_for_status()
        assert response.status_code == requests.codes.ok
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"failed to read {full_url}: {e}")
        return None


def location(connection: sqlite3.Connection):
    """
    Fetches all locations from the API and inserts them into the database.
    API에서 모든 위치 정보를 가져와 데이터베이스에 삽입합니다.

    :param connection: The sqlite3 database connection. sqlite3 데이터베이스 연결.
    """
    print("fetching location pages")
    cursor = connection.cursor()
    page = 0
    while True:
        page += 1
        response = read("/location", page)
        if response is None:
            break
        for result in response["results"]:
            id_ = result["id"]
            residents = result["residents"]
            # https://github.com/afuh/rick-and-morty-api/issues/140
            if id_ == 35:
                character_125 = "https://rickandmortyapi.com/api/character/125"
                if character_125 not in residents:
                    residents.append(character_125)
            cursor.execute(
                """INSERT INTO location
                       (id, name, type, dimension, residents, url, created)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    id_,
                    result["name"],
                    result["type"].strip() or None,
                    result["dimension"].strip() or None,
                    ",".join(residents).strip() or None,
                    result["url"],
                    result["created"],
                ),
            )
    connection.commit()


def character(connection: sqlite3.Connection):
    """
    Fetches all characters from the API and inserts them into the database.
    API에서 모든 캐릭터 정보를 가져와 데이터베이스에 삽입합니다.

    :param connection: The sqlite3 database connection. sqlite3 데이터베이스 연결.
    """
    print("fetching character pages")
    cursor = connection.cursor()
    page = 0
    while True:
        page += 1
        response = read("/character", page)
        if response is None:
            break
        for result in response["results"]:
            id_ = result["id"]
            origin_name = result["origin"]["name"]
            origin_url = result["origin"]["url"].strip() or None
            if origin_url is None:
                assert origin_name == 'unknown'
                origin_name = None
            location_name = result["location"]["name"]
            location_url = result["location"]["url"].strip() or None
            if location_url is None:
                assert location_name == 'unknown'
                location_name = None
            origin_id_ = origin_url.split("/")[-1] if origin_url is not None else None
            location_id_ = location_url.split("/")[-1] if location_url is not None else None
            episode = result["episode"]
            if id_ == 663:
                # https://github.com/afuh/rick-and-morty-api/issues/142
                episode_10 = "https://rickandmortyapi.com/api/episode/10"
                if episode_10 not in episode:
                    episode.append(episode_10)
            cursor.execute(
                """INSERT INTO character
                   (id, name, status, species, type, gender,
                    origin_name, origin_url,
                    location_name, location_url,
                    image, episode, url, created,
                    origin_id_, location_id_)
                   VALUES (?, ?, ?, ?, ?, ?,
                           ?, ?,
                           ?, ?,
                           ?, ?, ?, ?,
                           ?, ?)""",
                (
                    id_,
                    result["name"],
                    result["status"],
                    result["species"],
                    result["type"].strip() or None,
                    result["gender"],
                    origin_name,
                    origin_url,
                    location_name,
                    location_url,
                    result["image"],
                    ",".join(episode),
                    result["url"],
                    result["created"],
                    origin_id_,
                    location_id_,
                ),
            )
    connection.commit()


def episode(connection: sqlite3.Connection):
    """
    Fetches all episodes from the API and inserts them into the database.
    API에서 모든 에피소드 정보를 가져와 데이터베이스에 삽입합니다.

    :param connection: The sqlite3 database connection. sqlite3 데이터베이스 연결.
    """
    print("fetching episode pages")
    cursor = connection.cursor()
    page = 0
    while True:
        page += 1
        response = read("/episode", page)
        if response is None:
            break
        for result in response["results"]:
            air_date = result["air_date"]
            air_date_iso_ = datetime.datetime.strptime(air_date, "%B %d, %Y").strftime("%Y-%m-%d")
            id_ = result["id"]
            characters = result["characters"]
            if id_ == 18 or id_ == 21:
                # https://github.com/afuh/rick-and-morty-api/issues/141
                character_125 = "https://rickandmortyapi.com/api/character/125"
                if character_125 not in characters:
                    characters.append(character_125)
            cursor.execute(
                """INSERT INTO episode
                   (id, name, air_date, episode, characters,
                    url, created,
                    air_date_iso_)
                   VALUES (?, ?, ?, ?, ?,
                           ?, ?,
                           ?)""",
                (
                    id_,
                    result["name"],
                    air_date,
                    result["episode"],
                    ",".join(characters),
                    result["url"],
                    result["created"],
                    air_date_iso_,
                ),
            )
    connection.commit()


def location_resident(connection: sqlite3.Connection):
    """
    Populates the location_resident mapping table based on the location table.
    location 테이블을 기반으로 location_resident 매핑 테이블을 채웁니다.

    :param connection: The sqlite3 database connection. sqlite3 데이터베이스 연결.
    """
    cursor = connection.cursor()
    cursor.execute("""SELECT id, residents
                      FROM location
                      ORDER BY id ASC""")
    for each in cursor.fetchall():
        id_ = each[0]
        residents = each[1]
        if residents is None:
            continue
        for resident_id in sorted(
                [e.split("/")[-1] for e in residents.split(",")], key=int
        ):
            cursor.execute(
                """INSERT INTO location_resident (location_id, resident_id)
                   VALUES (?, ?)""",
                (id_, resident_id),
            )
    connection.commit()


def character_episode(connection: sqlite3.Connection):
    """
    Populates the character_episode mapping table based on the character table.
    character 테이블을 기반으로 character_episode 매핑 테이블을 채웁니다.

    :param connection: The sqlite3 database connection. sqlite3 데이터베이스 연결.
    """
    cursor = connection.cursor()
    cursor.execute("""SELECT id, episode
                      FROM character
                      ORDER BY id ASC""")
    for each in cursor.fetchall():
        id_ = each[0]
        episode = each[1]
        if episode is None:
            continue
        for episode_id in sorted(
                [e.split("/")[-1] for e in episode.split(",")], key=int
        ):
            cursor.execute(
                """INSERT INTO character_episode (character_id, episode_id)
                   VALUES (?, ?)""",
                (id_, episode_id),
            )
    connection.commit()


def episode_character(connection: sqlite3.Connection):
    """
    Populates the episode_character mapping table based on the episode table.
    episode 테이블을 기반으로 episode_character 매핑 테이블을 채웁니다.

    :param connection: The sqlite3 database connection. sqlite3 데이터베이스 연결.
    """
    cursor = connection.cursor()
    cursor.execute("""SELECT id, characters
                      FROM episode
                      ORDER BY id ASC""")
    for each in cursor.fetchall():
        id_ = each[0]
        characters = each[1]
        if characters is None:
            continue
        for character_id in sorted(
                [e.split("/")[-1] for e in characters.split(",")], key=int
        ):
            cursor.execute(
                """INSERT INTO episode_character (episode_id, character_id)
                   VALUES (?, ?)""",
                (id_, character_id),
            )
    connection.commit()


def finalize(connection: sqlite3.Connection):
    """
    Performs maintenance tasks on the database: REINDEX, VACUUM, and integrity check.
    데이터베이스 유지 관리 작업을 수행합니다: REINDEX, VACUUM 및 무결성 검사.

    :param connection: The sqlite3 database connection. sqlite3 데이터베이스 연결.
    :return: True if the database is intact, False otherwise.
             데이터베이스가 온전하면 True, 그렇지 않으면 False.
    """
    cursor = connection.cursor()
    cursor.execute("REINDEX")
    print(f"database '{db_file}' successfully REINDEX-ed")
    cursor.execute("VACUUM")
    print(f"database '{db_file}' successfully VACUUM-ed")
    cursor.execute('PRAGMA integrity_check')
    results = cursor.fetchall()
    if len(results) == 1 and results[0][0] == 'ok':
        print(f"database '{db_file}' is intact and not corrupted.")
        return True
    else:
        print(f"database '{db_file}' is corrupted. details:")
        for row in results:
            print(f"- {row[0]}")
        return False


def count(connection: sqlite3.Connection, table: str):
    """
    Counts the number of rows in a specified table.
    지정된 테이블의 행 수를 셉니다.

    :param connection: The sqlite3 database connection. sqlite3 데이터베이스 연결.
    :param table: The name of the table to count rows from. 행 수를 셀 테이블의 이름.
    :return: The number of rows, or None if the result is unavailable.
             행의 수, 또는 결과를 사용할 수 없는 경우 None.
    """
    cursor = connection.cursor()
    query = f"SELECT COUNT(*) FROM {table}"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else None


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="enable debug logging")
    args = parser.parse_args()
    create()
    connect(location)
    connect(character)
    connect(episode)
    connect(location_resident)
    connect(character_episode)
    connect(episode_character)
    connect(finalize)
    location_count = connect(lambda c: count(c, "location"))
    print(f"location count: {location_count}")
    assert location_count == 126
    character_count = connect(lambda c: count(c, "character"))
    print(f"character count: {character_count}")
    assert character_count == 826
    episode_count = connect(lambda c: count(c, "episode"))
    print(f"episode count: {episode_count}")
    assert episode_count == 51
