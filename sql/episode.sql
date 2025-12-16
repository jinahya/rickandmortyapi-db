--


-- ------------------------------------------------------------------------------------------------------------------ id

-- ---------------------------------------------------------------------------------------------------------------- name

-- ------------------------------------------------------------------------------------------------------------ air_date


-- ------------------------------------------------------------------------------------------------------- air_date_iso_
-- have `id` and `air_date_iso` the same order?
SELECT COUNT(*) AS differences_count
FROM (SELECT id,
             air_date_iso_,
             ROW_NUMBER() OVER (ORDER BY id ASC)                    AS seqnum_id,
             ROW_NUMBER() OVER (ORDER BY air_date_iso_ ASC, id ASC) AS seqnum_date
      FROM episode) AS T
WHERE seqnum_id <> seqnum_date
;

-- ------------------------------------------------------------------------------------------------------------- episode
-- have `id` and `episode` the same order?
SELECT COUNT(*) AS differences_count
FROM (SELECT id,
             episode,
             ROW_NUMBER() OVER (ORDER BY id ASC)              AS seqnum_id,
             ROW_NUMBER() OVER (ORDER BY episode ASC, id ASC) AS seqnum_date
      FROM episode) AS T
WHERE seqnum_id <> seqnum_date
;

-- ---------------------------------------------------------------------------------------------------------- characters
-- episode_character - character; should be empty
SELECT *
FROM episode e
         JOIN episode_character ec ON e.id = ec.episode_id
         LEFT OUTER JOIN character c ON ec.character_id = c.id
WHERE c.id IS NULL
;

-- ----------------------------------------------------------------------------------------------------------------- url

-- ------------------------------------------------------------------------------------------------------------- created