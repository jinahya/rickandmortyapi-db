--


-- ------------------------------------------------------------------------------------------------------------------ id

-- ---------------------------------------------------------------------------------------------------------------- name

-- ---------------------------------------------------------------------------------------------------------------- type
SELECT *
FROM location
WHERE type IS NULL
;

SELECT DISTINCT type
FROM location
ORDER BY type ASC
;

SELECT type, count(*) as count
FROM location
GROUP BY type
ORDER BY count DESC
;

-- ----------------------------------------------------------------------------------------------------------- dimension
SELECT *
FROM location
WHERE dimension IS NULL
;

SELECT DISTINCT dimension
FROM location
ORDER BY dimension ASC
;

SELECT dimension, count(*) as count
FROM location
GROUP BY dimension
ORDER BY count DESC
;

-- ----------------------------------------------------------------------------------------------------------- residents
SELECT *
FROM location
WHERE residents IS NULL
;

-- ----------------------------------------------------------------------------------------------------------------- url

-- ------------------------------------------------------------------------------------------------------------- created