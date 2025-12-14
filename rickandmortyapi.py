import datetime
import json
import os
import requests
import sqlite3


# use with connection.set_trace_callback(log_sql_callback)
def log_sql_callback(statement):
    print(f"Executing SQL statement: {statement}")


db_file = "rickandmortyapi.db"


def create():
    sql_file = "rickandmortyapi.sql"
    if os.path.exists(db_file):
        print(f"removing existing database file: '{db_file}'")
        os.remove(db_file)
    connection = None
    try:
        with open(sql_file, "r", encoding="utf-8") as f:
            sql_script = f.read()
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
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
    print(f"fetching {full_url}")
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
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        # connection.set_trace_callback(log_sql_callback)
        cursor = connection.cursor()
        page = 1
        while True:
            response = read("/location", page)
            if response is None:
                break
            for result in response["results"]:
                cursor.execute(
                    """INSERT INTO location
                           (id, name, type, dimension, residents, url, created)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        result["id"],
                        result["name"],
                        result["type"].strip() or None,
                        result["dimension"].strip() or None,
                        ",".join(result["residents"]).strip() or None,
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
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        # connection.set_trace_callback(log_sql_callback)
        cursor = connection.cursor()
        page = 1
        while True:
            response = read("/character", page)
            if response is None:
                break
            for result in response["results"]:
                origin_name= result["origin"]["name"]
                origin_url= result["origin"]["url"]
                location_name= result["location"]["name"]
                location_url= result["location"]["url"]
                _origin_id = origin_url.split("/")[-1] or None
                _location_id = location_url.split("/")[-1] or None
                cursor.execute(
                    """INSERT INTO character
                       (id, name, status, species, type, gender,
                        origin_name, origin_url,
                        location_name, location_url,
                        image, episode, url, created,
                        _origin_id, _location_id)
                       VALUES (?, ?, ?, ?, ?, ?,
                               ?, ?,
                               ?, ?,
                               ?, ?, ?, ?,
                               ?, ?)""",
                    (
                        result["id"],
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
                        ",".join(result["episode"]),
                        result["url"],
                        result["created"],
                        _origin_id,
                        _location_id,
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
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        # connection.set_trace_callback(log_sql_callback)
        cursor = connection.cursor()
        page = 1
        while True:
            response = read("/episode", page)
            if response is None:
                break
            for result in response["results"]:
                air_date = result["air_date"]
                _air_date_iso = datetime.datetime.strptime(
                    air_date, "%B %d, %Y"
                ).strftime("%Y-%m-%d")
                cursor.execute(
                    """INSERT INTO episode
                           (id, name, air_date, episode, characters, url, created, _air_date_iso)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        result["id"],
                        result["name"],
                        air_date,
                        result["episode"],
                        ",".join(result["characters"]),
                        result["url"],
                        result["created"],
                        _air_date_iso,
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


# def character():
#     connection = None
#     try:
#         connection = sqlite3.connect(db_file)
#         # connection.set_trace_callback(log_sql_callback)
#         cursor = connection.cursor()
#         page = 1
#         while True:
#             response = read("/character", page)
#             if response is None:
#                 break
#             for result in response["results"]:
#                 cursor.execute(
#                     """INSERT INTO character
#                        (id, name, status, species, type, gender, origin, location, image, episode, url, created,
#                         _origin_id, _location_id)
#                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
#                     (
#                         result["id"],
#                         result["name"],
#                         result["status"],
#                         result["species"],
#                         result["type"].strip() or None,
#                         result["gender"],
#                         json.dumps(result["origin"]),
#                         json.dumps(result["location"]),
#                         result["image"],
#                         ",".join(result["episode"]),
#                         result["url"],
#                         result["created"],
#                         result["origin"]["url"].split("/")[-1] or None,
#                         result["location"]["url"].split("/")[-1] or None,
#                     ),
#                 )
#             page += 1
#         connection.commit()
#     except sqlite3.Error as e:
#         print(f"a database error occurred: {e}")
#     except IOError as e:
#         print(f"an error reading the SQL file occurred: {e}")
#     finally:
#         if connection:
#             connection.close()


def location_resident():
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        # connection.set_trace_callback(log_sql_callback)
        cursor = connection.cursor()
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
        cursor.execute("""SELECT id, characters
                          FROM episode
                          ORDER BY id ASC""")
        for each in cursor.fetchall():
            id = each[0]
            characters = each[1]
            if characters is None:
                continue
            for character_id in sorted(
                    [e.split("/")[-1] for e in characters.split(",")], key=int
            ):
                cursor.execute(
                    """INSERT INTO episode_character (episode_id, character_id)
                       VALUES (?, ?)""",
                    (id, character_id),
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
    try:
        connection = sqlite3.connect(db_file, isolation_level=None)
        cursor = connection.cursor()
        cursor.execute("VACUUM")
        print(f"database '{db_file}' successfully vacuumed")
    except sqlite3.Error as e:
        print(f"an error occurred during VACUUM: {e}")
    finally:
        if connection:
            connection.close()


def reindex():
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        cursor.execute("REINDEX;")
        print(f"database '{db_file}' successfully REINDEX-ed")
    except sqlite3.Error as e:
        print(f"an SQLite error occurred: {e}")
        return False
    finally:
        if connection:
            connection.close()


def check():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Execute the integrity check PRAGMA
        cursor.execute('PRAGMA integrity_check;')

        # Fetch all results. The PRAGMA returns one or more rows.
        # If everything is "ok", it returns a single row with the value "ok".
        results = cursor.fetchall()

        # Check if the result is "ok"
        if len(results) == 1 and results[0][0] == 'ok':
            print(f"database '{db_file}' is intact and not corrupted.")
            return True
        else:
            print(f"database '{db_file}' is corrupted. details:")
            for row in results:
                print(f"- {row[0]}")
            return False

    except sqlite3.Error as e:
        print(f"an SQLite error occurred: {e}")
        return False
    finally:
        if connection:
            connection.close()


def count(table):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        query = f"SELECT COUNT(*) FROM {table}"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        print(f"an error occurred while counting: {table} {e}")
    finally:
        if connection:
            connection.close()


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
