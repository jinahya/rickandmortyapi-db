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

-- ----------------------------------------------------------------------------------------------------------------- url

-- ------------------------------------------------------------------------------------------------------------- created