--


-- ---------------------------------------------------------------------------------------------------------- episode_id
SELECT *
FROM episode_character ec
         LEFT OUTER JOIN main.episode e ON ec.episode_id = e.id
WHERE e.id IS NULL
;


-- -------------------------------------------------------------------------------------------------------- character_id
SELECT *
FROM episode_character ec
         LEFT OUTER JOIN character c ON ec.character_id = c.id
WHERE c.id IS NULL
;

SELECT episode_id, COUNT(1) AS character_count, GROUP_CONCAT(c.id || '(' || c.name || ')' ORDER BY c.id)
FROM episode_character ec
         JOIN character c ON ec.character_id = c.id
GROUP BY episode_id
-- HAVING character_count > 1
ORDER BY character_count DESC
;

SELECT episode_id, character_id
FROM episode_character
GROUP BY episode_id
;



-- 1: Rick Sanchez
-- 2: Morty Smith
-- 3: Summer Smith
-- 4: Beth Smith
-- 5: Jerry Smith

SELECT ec.episode_id, GROUP_CONCAT(ec.character_id) character_ids, GROUP_CONCAT(c.name) character_names
FROM episode_character ec
         JOIN character c ON ec.character_id = c.id
WHERE ec.character_id IN (4, 5)
GROUP BY ec.episode_id
HAVING COUNT(DISTINCT ec.character_id) = 2
;

SELECT ec.episode_id, GROUP_CONCAT(ec.character_id) character_ids, GROUP_CONCAT(c.name) character_names
FROM episode_character ec
         JOIN character c ON ec.character_id = c.id
WHERE ec.character_id IN (1, 2, 4)
GROUP BY ec.episode_id
HAVING COUNT(DISTINCT ec.character_id) = 3
;

SELECT ec.episode_id, GROUP_CONCAT(ec.character_id) character_ids, GROUP_CONCAT(c.name) character_names
FROM episode_character ec
         JOIN character c ON ec.character_id = c.id
WHERE ec.character_id IN (1, 2, 5)
GROUP BY ec.episode_id
HAVING COUNT(DISTINCT ec.character_id) = 3
;

SELECT ec.episode_id, GROUP_CONCAT(ec.character_id) character_ids, GROUP_CONCAT(c.name) character_names
FROM episode_character ec
         JOIN character c ON ec.character_id = c.id
WHERE ec.character_id IN (1, 2, 3, 4)
GROUP BY ec.episode_id
HAVING COUNT(DISTINCT ec.character_id) = 4
;

SELECT ec.episode_id, GROUP_CONCAT(ec.character_id) character_ids, GROUP_CONCAT(c.name) character_names
FROM episode_character ec
         JOIN character c ON ec.character_id = c.id
WHERE ec.character_id IN (1, 2, 3, 4, 5)
GROUP BY ec.episode_id
HAVING COUNT(DISTINCT c.id) = 5
;



-- ---------------------------------------------------------------------------------------------------------------------
-- should be empty
SELECT *
FROM episode_character ec
         LEFT OUTER JOIN character_episode ce ON ec.episode_id = ce.episode_id AND ec.character_id = ce.character_id
WHERE ce.character_id IS NULL
;

