import datetime
import os
import requests
import sqlite3
from typing import Callable, Any


# use with connection.set_trace_callback(log_sql_callback)
def log_sql_callback(statement):
    print(f"Executing SQL statement: {statement}")


db_file = "rickandmortyapi.db"


def connect(operation: Callable[[sqlite3.Connection], Any]) -> Any:
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        # connection.set_trace_callback(log_sql_callback)
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
    sql_file = "rickandmortyapi-db.sql"
    if os.path.exists(db_file):
        print(f"removing existing database file: '{db_file}'")
        os.remove(db_file)
    connection = None
    try:
        with open(sql_file, "r", encoding="utf-8") as f:
            sql_script = f.read()
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        print(f"new database '{db_file}' created and connected")
        cursor.executescript(sql_script)
        connection.commit()
        print(f"successfully executed DDL script from '{sql_file}'")
    except sqlite3.Error as e:
        print(f"a database error occurred: {e}")
    except IOError as e:
        print(f"an error reading the SQL file occurred: {e}")
    finally:
        if connection:
            connection.close()


base_url = "https://rickandmortyapi.com/api"


def read(path, page=1):
    full_url = f"{base_url}{path}?page={page}"
    # print(f"fetching {full_url}")
    try:
        response = requests.get(full_url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"failed to read {full_url}: {e}")
        return None


def location():
    print("fetching location pages")
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        page = 1
        while True:
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
            page += 1
        connection.commit()
    except sqlite3.Error as e:
        print(f"a database error occurred: {e}")
    except IOError as e:
        print(f"an error reading the SQL file occurred: {e}")
    finally:
        if connection:
            connection.close()


def character():
    print("fetching character pages")
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        page = 1
        while True:
            response = read("/character", page)
            if response is None:
                break
            for result in response["results"]:
                id_ = result["id"]
                origin_name = result["origin"]["name"]
                origin_url = result["origin"]["url"].strip() or None
                location_name = result["location"]["name"]
                location_url = result["location"]["url"].strip() or None
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
            page += 1
        connection.commit()
    except sqlite3.Error as e:
        print(f"a database error occurred: {e}")
    except IOError as e:
        print(f"an error reading the SQL file occurred: {e}")
    finally:
        if connection:
            connection.close()


def episode():
    print("fetching episode pages")
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        page = 1
        while True:
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
            page += 1
        connection.commit()
    except sqlite3.Error as e:
        print(f"a database error occurred: {e}")
    except IOError as e:
        print(f"an error reading the SQL file occurred: {e}")
    finally:
        if connection:
            connection.close()


def location_resident():
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("""SELECT id, residents
                          FROM location
                          ORDER BY id ASC""")
        for each in cursor.fetchall():
            id = each[0]
            residents = each[1]
            if residents is None:
                continue
            for resident_id in sorted(
                    [e.split("/")[-1] for e in residents.split(",")], key=int
            ):
                cursor.execute(
                    """INSERT INTO location_resident (location_id, resident_id)
                       VALUES (?, ?)""",
                    (id, resident_id),
                )
        connection.commit()
    except sqlite3.Error as e:
        print(f"a database error occurred: {e}")
    except IOError as e:
        print(f"an error reading the SQL file occurred: {e}")
    finally:
        if connection:
            connection.close()


def character_episode():
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("""SELECT id, episode
                          FROM character
                          ORDER BY id ASC""")
        for each in cursor.fetchall():
            id = each[0]
            episode = each[1]
            if episode is None:
                continue
            for episode_id in sorted(
                    [e.split("/")[-1] for e in episode.split(",")], key=int
            ):
                cursor.execute(
                    """INSERT INTO character_episode (character_id, episode_id)
                       VALUES (?, ?)""",
                    (id, episode_id),
                )
        connection.commit()
    except sqlite3.Error as e:
        print(f"a database error occurred: {e}")
    except IOError as e:
        print(f"an error reading the SQL file occurred: {e}")
    finally:
        if connection:
            connection.close()


def episode_character():
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
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
    except sqlite3.Error as character_id:
        print(f"a database error occurred: {character_id}")
    except IOError as character_id:
        print(f"an error reading the SQL file occurred: {character_id}")
    finally:
        if connection:
            connection.close()


def vacuum():
    def op(c: sqlite3.Connection):
        cursor = c.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("VACUUM")
        print(f"database '{db_file}' successfully vacuumed")

    connect(op)


def reindex():
    def op(c: sqlite3.Connection):
        cursor = c.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("REINDEX")
        print(f"database '{db_file}' successfully REINDEX-ed")

    try:
        connect(op)
    except sqlite3.Error:
        return False
    return True


def check():
    def op(c: sqlite3.Connection):
        cursor = c.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
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

    try:
        return connect(op)
    except sqlite3.Error:
        return False


def count(table):
    def op(c: sqlite3.Connection):
        cursor = c.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        query = f"SELECT COUNT(*) FROM {table}"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None

    try:
        return connect(op)
    except sqlite3.Error as e:
        print(f"an error occurred while counting: {table} {e}")
        return None


# ----------------------------------------------------------------------------------------------------------------------
create()

# ----------------------------------------------------------------------------------------------------------------------
location()
character()
episode()

location_resident()
character_episode()
episode_character()

# ----------------------------------------------------------------------------------------------------------------------
vacuum()
reindex()
check()

# ----------------------------------------------------------------------------------------------------------------------
location_count = count("location")
print(f"location count: {location_count}")
assert location_count == 126

character_count = count("character")
print(f"character count: {character_count}")
assert character_count == 826

episode_count = count("episode")
print(f"episode count: {episode_count}")
assert episode_count == 51
