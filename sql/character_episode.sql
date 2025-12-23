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
