--
-- https://rickandmortyapi.com/documentation


-- ------------------------------------------------------------------------------------------------------------ location
-- https://rickandmortyapi.com/documentation/#location-schema
-- https://rickandmortyapi.com/api/location
CREATE TABLE IF NOT EXISTS location
(
    id        INTEGER NOT NULL PRIMARY KEY, -- $.id
    name      TEXT    NOT NULL,             -- $.name
    type      TEXT    NULL,                 -- $.type
    dimension TEXT    NULL,                 -- $.dimension
    residents TEXT    NULL,                 -- $.residents
    url       TEXT    NOT NULL UNIQUE,      -- $.url
    created   TEXT    NOT NULL              -- $.created
);

CREATE INDEX location_type_index ON location (type);
CREATE INDEX location_dimension_index ON location (dimension);
CREATE INDEX location_created_index ON location (created);


-- ----------------------------------------------------------------------------------------------------------- character
-- https://rickandmortyapi.com/documentation/#character-schema
-- https://rickandmortyapi.com/api/character
CREATE TABLE IF NOT EXISTS character
(
    id            INTEGER NOT NULL PRIMARY KEY, -- $.id
    name          TEXT    NOT NULL,             -- $.name
    status        TEXT    NOT NULL,             -- $.status
    species       TEXT    NOT NULL,             -- $.species
    type          TEXT    NULL,                 -- $.type
    gender        TEXT    NOT NULL,             -- $.gender
    origin_name   TEXT    NULL,                 -- $.origin.name
    origin_url    TEXT    NULL,                 -- $.origin.url
    location_name TEXT    NULL,                 -- $.location.name
    location_url  TEXT    NULL,                 -- $.location.url
    image         TEXT    NOT NULL UNIQUE,      -- $.image
    episode       TEXT    NOT NULL,             -- $.episode
    url           TEXT    NOT NULL UNIQUE,      -- $.url
    created       TEXT    NOT NULL,             -- $.created
    origin_id_    INTEGER NULL,                 -- location.id mapped by $.origin.url
    location_id_  INTEGER NULL,                 -- location.id mapped by $.location.url
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


-- ------------------------------------------------------------------------------------------------------------- episode
-- https://rickandmortyapi.com/documentation/#episode-schema
-- https://rickandmortyapi.com/api/episode
CREATE TABLE IF NOT EXISTS episode
(
    id            INTEGER NOT NULL PRIMARY KEY, -- $.id
    name          TEXT    NOT NULL,             -- $.name
    air_date      TEXT    NOT NULL,             -- $.air_date
    episode       TEXT    NOT NULL UNIQUE,      -- $.episode
    characters    TEXT    NOT NULL,             -- $.characters
    url           TEXT    NOT NULL UNIQUE,      -- $.url
    created       TEXT    NOT NULL,             -- $.created
    air_date_iso_ TEXT    NOT NULL              -- ISO 8601 date format of the `air_date`
);

CREATE INDEX episode_created_index ON episode (created);
CREATE INDEX episode_air_date_iso__index ON episode (air_date_iso_);


-- --------------------------------------------------------------------------------------------------- location_resident
-- /api/location
CREATE TABLE IF NOT EXISTS location_resident
(
    location_id INTEGER NOT NULL, -- $.id
    resident_id INTEGER NOT NULL, -- character.id mapped by $.residents[*].id
    PRIMARY KEY (location_id, resident_id),
    FOREIGN KEY (location_id) REFERENCES location (id),
    FOREIGN KEY (resident_id) REFERENCES character (id)
);

CREATE INDEX location_resident_resident_id_index ON location_resident (resident_id);

-- --------------------------------------------------------------------------------------------------- character_episode
-- /api/character
CREATE TABLE IF NOT EXISTS character_episode
(
    character_id INTEGER NOT NULL, -- $.id
    episode_id   INTEGER NOT NULL, -- episode.id mapped by $.episode[*].id
    PRIMARY KEY (character_id, episode_id),
    FOREIGN KEY (character_id) REFERENCES character (id),
    FOREIGN KEY (episode_id) REFERENCES episode (id)
);

CREATE INDEX character_episode_episode_id_index ON character_episode (episode_id);


-- --------------------------------------------------------------------------------------------------- episode_character
-- /api/episode
CREATE TABLE IF NOT EXISTS episode_character
(
    episode_id   INTEGER NOT NULL, -- $.id
    character_id INTEGER NOT NULL, -- $.characters[*].id
    PRIMARY KEY (episode_id, character_id),
    FOREIGN KEY (episode_id) REFERENCES episode (id),
    FOREIGN KEY (character_id) REFERENCES character (id)
);

CREATE INDEX episode_character_character_id_index ON episode_character (character_id);