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

CREATE INDEX location_type_index ON location (type);
CREATE INDEX location_dimension_index ON location (dimension);
CREATE INDEX location_created_index ON location (created);

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
    origin_url    TEXT NULL,     -- $.origin.url
    location_name TEXT NOT NULL, -- $.location.name
    location_url  TEXT NULL,     -- $.location.url
    image         TEXT NOT NULL UNIQUE,
    episode       TEXT NOT NULL,
    url           TEXT NOT NULL UNIQUE,
    created       TEXT NOT NULL,
    origin_id_    INTEGER,       -- location.id for the $.origin.url
    location_id_  INTEGER,       -- location.id for the $.location.url
    FOREIGN KEY (origin_id_) REFERENCES location (id),
    FOREIGN KEY (location_id_) REFERENCES location (id)
);

CREATE INDEX character_status_index ON character (status);

CREATE INDEX character_species_index ON character (species);

CREATE INDEX character_type_index ON character (type);

CREATE INDEX character_gender_index ON character (gender);

CREATE INDEX character_created_index ON character (created);

CREATE INDEX character_origin_id__index ON character (origin_id_);

CREATE INDEX character_location_id__index ON character (location_id_);

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
    air_date_iso_ TEXT NOT NULL -- ISO 8601 date format of the `air_date`
);

CREATE INDEX episode_created_index ON episode (created);

CREATE INDEX episode_air_date_iso__index ON episode (air_date_iso_);

-- ---------------------------------------------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS location_resident
    -- mapping from the $.residents
(
    location_id INTEGER NOT NULL,
    resident_id INTEGER NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location (id),
    FOREIGN KEY (resident_id) REFERENCES character (id),
    UNIQUE (location_id, resident_id),
    UNIQUE (resident_id, location_id)
);

-- CREATE INDEX location_resident_resident_id_index ON location_resident (resident_id);

-- --------------------------------------------------------------------------------------------------- character.episode
CREATE TABLE IF NOT EXISTS character_episode
    -- mapping from the $.episode
(
    character_id INTEGER NOT NULL,
    episode_id   INTEGER NOT NULL,
    FOREIGN KEY (character_id) REFERENCES character (id),
    FOREIGN KEY (episode_id) REFERENCES episode (id),
    UNIQUE (character_id, episode_id),
    UNIQUE (episode_id, character_id)
);

-- CREATE INDEX character_episode_episode_id_index ON character_episode (episode_id);


-- -------------------------------------------------------------------------------------------------- episode.characters
CREATE TABLE IF NOT EXISTS episode_character
    -- mapping from the $.characters
(
    episode_id   INTEGER NOT NULL,
    character_id INTEGER NOT NULL,
    FOREIGN KEY (episode_id) REFERENCES episode (id),
    FOREIGN KEY (character_id) REFERENCES character (id),
    UNIQUE (episode_id, character_id),
    UNIQUE (character_id, episode_id)
);

-- CREATE INDEX episode_character_character_id_index ON episode_character (character_id);
