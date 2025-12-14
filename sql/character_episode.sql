--

-- -------------------------------------------------------------------------------------------------------- character_id
EXPLAIN QUERY PLAN
SELECT ce.character_id, c.id
FROM character_episode ce
         LEFT OUTER JOIN character c ON ce.character_id = c.id
WHERE c.id IS NULL
;


-- ---------------------------------------------------------------------------------------------------------- episode_id
EXPLAIN QUERY PLAN
SELECT ce.episode_id, e.id
FROM character_episode ce
         LEFT OUTER JOIN main.episode e ON ce.episode_id = e.id
WHERE e.id IS NULL
;
