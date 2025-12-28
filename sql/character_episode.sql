--

-- -------------------------------------------------------------------------------------------------------- character_id
-- episode_count by character_id
SELECT character_id, COUNT(1) episode_count
FROM character_episode
GROUP BY character_id
HAVING episode_count > 1
ORDER BY episode_count DESC
;

EXPLAIN QUERY PLAN
SELECT ce.character_id, c.id
FROM character_episode ce
         LEFT OUTER JOIN character c ON ce.character_id = c.id
WHERE c.id IS NULL
;


-- ---------------------------------------------------------------------------------------------------------- episode_id
-- character_count by episode_id
SELECT episode_id, COUNT(1) character_count
FROM character_episode
GROUP BY episode_id
HAVING character_count > 1
ORDER BY character_count DESC
;

-- given episodes, find characters have been seen all episodes
SELECT c.*
FROM character_episode ce
         JOIN character c ON c.id = ce.character_id
WHERE ce.episode_id IN (1, 2, 38, 175, 338)
GROUP BY ce.character_id
HAVING COUNT(DISTINCT ce.episode_id) = 5
;

EXPLAIN QUERY PLAN
SELECT ce.episode_id, e.id
FROM character_episode ce
         LEFT OUTER JOIN main.episode e ON ce.episode_id = e.id
WHERE e.id IS NULL
;

-- ---------------------------------------------------------------------------------------------------------------------
-- should be empty
SELECT *
FROM character_episode ce
         LEFT OUTER JOIN episode_character ec ON ce.character_id = ec.character_id AND ce.episode_id = ec.episode_id
WHERE ec.episode_id IS NULL
;


-- ---------------------------------------------------------------------------------------------------------------------

-- 1: Rick Sanchez
-- 2: Morty Smith
-- 3: Summer Smith
-- 4: Beth Smith
-- 5: Jerry Smith


-- given episodes, find characters have been seen all episodes
SELECT c.*
FROM character c
         JOIN character_episode ce ON c.id = ce.character_id
WHERE ce.episode_id IN (1, 2, 38, 175, 338)
GROUP BY c.id, c.name
HAVING COUNT(DISTINCT ce.episode_id) = 5
;

SELECT character_id
FROM character_episode
WHERE episode_id IN (1, 2, 38, 175, 338)
GROUP BY character_id
HAVING COUNT(DISTINCT episode_id) = 5
;
