--

-- ---------------------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS location
(
    id        INTEGER PRIMARY KEY,
    name      TEXT NOT NULL,
    type      TEXT,
    dimension TEXT,
    residents TEXT,
    url       TEXT NOT NULL UNIQUE,
    created   TEXT NOT NULL
);

CREATE INDEX location_created ON location (created);

-- ---------------------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS character
(
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    status        TEXT NOT NULL,
    species       TEXT NOT NULL,
    type          TEXT,
    gender        TEXT NOT NULL,
    origin_name   TEXT NOT NULL, -- $.origin.name
    origin_url    TEXT NOT NULL, -- $.origin.url
    location_name TEXT NOT NULL, -- $.location.name
    location_url  TEXT NOT NULL, -- $.location.url
    image         TEXT NOT NULL,
    episode       TEXT NOT NULL,
    url           TEXT NOT NULL UNIQUE,
    created       TEXT NOT NULL,
    _origin_id    INTEGER,       -- location.id for the $.origin.url
    _location_id  INTEGER,       -- location.id for the $.location.url
    FOREIGN KEY (_origin_id) REFERENCES location (id),
    FOREIGN KEY (_location_id) REFERENCES location (id)
);

CREATE INDEX character_created_index ON character (created);

CREATE INDEX character__origin_id_index ON character (_origin_id);

CREATE INDEX character__location_id_index ON character (_location_id);

-- ---------------------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS episode
(
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    air_date      TEXT NOT NULL,
    episode       TEXT NOT NULL UNIQUE,
    characters    TEXT NOT NULL,
    url           TEXT NOT NULL UNIQUE,
    created       TEXT NOT NULL,
    _air_date_iso TEXT NOT NULL -- ISO 8601 date format of the `air_date`
);

CREATE INDEX episode_created_index ON episode (created);

CREATE INDEX episode__air_date_iso_index ON episode (_air_date_iso);

-- ---------------------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS location_resident
    -- mapping from the $.residents
(
    location_id INTEGER NOT NULL,
    resident_id INTEGER NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location (id),
    FOREIGN KEY (resident_id) REFERENCES character (id),
    UNIQUE (location_id, resident_id)
);

CREATE INDEX location_resident_resident_id_index ON location_resident (resident_id);

-- --------------------------------------------------------------------------------------------------- character.episode
CREATE TABLE IF NOT EXISTS character_episode
    -- mapping from the $.episode
(
    character_id INTEGER NOT NULL,
    episode_id   INTEGER NOT NULL,
    FOREIGN KEY (character_id) REFERENCES character (id),
    FOREIGN KEY (episode_id) REFERENCES episode (id),
    UNIQUE (character_id, episode_id)
);

CREATE INDEX character_episode_episode_id_index ON character_episode (episode_id);


-- -------------------------------------------------------------------------------------------------- episode.characters
CREATE TABLE IF NOT EXISTS episode_character
    -- mapping from the $.characters
(
    episode_id   INTEGER NOT NULL,
    character_id INTEGER NOT NULL,
    FOREIGN KEY (episode_id) REFERENCES episode (id),
    FOREIGN KEY (character_id) REFERENCES character (id),
    UNIQUE (episode_id, character_id)
);

CREATE INDEX episode_character_character_id_index ON episode_character (character_id);
