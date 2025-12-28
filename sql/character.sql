--

-- ------------------------------------------------------------------------------------------------------------------ id
SELECT *
FROM character
ORDER BY id ASC
;

-- ---------------------------------------------------------------------------------------------------------------- nane

-- -------------------------------------------------------------------------------------------------------------- status
SELECT DISTINCT status
FROM character
ORDER BY status ASC
;

SELECT status, COUNT(*) AS count
FROM character
GROUP BY status
ORDER BY count DESC
;


-- ------------------------------------------------------------------------------------------------------------- species
SELECT DISTINCT species
FROM character
Order by species ASC
;

SELECT species, COUNT(*) AS count
FROM character
GROUP BY species
ORDER BY count DESC
;


-- ---------------------------------------------------------------------------------------------------------------- type
SELECT DISTINCT type
FROM character
Order by type ASC
;

SELECT type, COUNT(*) AS count
FROM character
GROUP BY type
ORDER BY count DESC
;


-- -------------------------------------------------------------------------------------------------------------- gender
SELECT DISTINCT gender
FROM character
Order by gender ASC
;

SELECT gender, COUNT(*) AS count
FROM character
GROUP BY gender
ORDER BY count DESC
;


-- --------------------------------------------------------------------------------------------------------- origin_name

-- ---------------------------------------------------------------------------------------------------------- origin_url
-- should be empty
SELECT c.origin_url, l.url
FROM character c
         LEFT OUTER JOIN location l ON c.origin_url = l.url
WHERE c.origin_url IS NOT NULL
  AND l.url IS NULL
;

-- should be empty
SELECT c.origin_name, c.origin_url, l.name, l.url
FROM character c
         LEFT OUTER JOIN location l ON c.origin_url = l.url AND c.origin_name = l.name
WHERE c.origin_url IS NOT NULL
  AND c.origin_url IS NULL
;

SELECT origin_url, COUNT(*) AS count
FROM character
GROUP BY origin_url
ORDER BY count DESC
;

-- should be empty
SELECT *
FROM character
WHERE (origin_name IS NULL) != (origin_url IS NULL)
;


-- ------------------------------------------------------------------------------------------------------- location_name


-- -------------------------------------------------------------------------------------------------------- location_url
-- should be empty
SELECT c.location_url, l.url
FROM character c
         LEFT OUTER JOIN location l ON c.location_url = l.url
WHERE c.location_url IS NOT NULL
  AND l.url IS NULL
;

-- should be empty
SELECT c.location_name, c.location_url, l.name, l.url
FROM character c
         LEFT OUTER JOIN location l ON c.location_url = l.url AND c.location_name = l.name
WHERE c.location_url IS NOT NULL
  AND c.location_url IS NULL
;

SELECT location_url, COUNT(*) AS count
FROM character
GROUP BY location_url
ORDER BY count DESC
;

-- should be empty
SELECT *
FROM character
WHERE (location_url IS NULL) != (location_name IS NULL);


-- --------------------------------------------------------------------------------------------------------------- image
-- no duplicate images
SELECT image, COUNT(*) AS count
FROM character
GROUP BY image
HAVING count > 1
ORDER BY count DESC
;

-- ------------------------------------------------------------------------------------------------------------- episode
-- character_episode - episode; should be empty
SELECT *
FROM character c
         JOIN character_episode ce ON c.id = ce.character_id
         LEFT OUTER JOIN episode e ON ce.episode_id = e.id
WHERE e.id IS NULL
;

-- ----------------------------------------------------------------------------------------------------------------- url

-- ------------------------------------------------------------------------------------------------------------- created

-- ---------------------------------------------------------------------------------------------------------- origin_id_
-- unmapped origin - should be empty
SELECT c.name, l.name
FROM character c
         JOIN location l ON c.origin_id_ = l.id
WHERE c.origin_id_ IS NOT NULL
  AND l.id IS NULL
;


-- -------------------------------------------------------------------------------------------------------- location_id_
-- location_id_ -> location.id
SELECT c.name, l.name
FROM character c
         JOIN location l ON c.location_id_ = l.id
WHERE c.origin_id_ IS NOT NULL
  AND l.id IS NULL
;

-- location_id_ -> location_resident.(location_id, resident_id)
SELECT c.id, c.location_id_, lr.location_id, lr.resident_id
FROM character c
         LEFT OUTER JOIN location_resident lr ON c.location_id_ = lr.location_id AND c.id = lr.resident_id
-- WHERE c.location_id_ IS NOT NULL
--   AND lr.resident_id IS NULL
WHERE (c.location_id_ IS NULL) <> (lr.resident_id IS NULL)
;
