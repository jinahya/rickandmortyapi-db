# SQL Solutions

## Caveats

The content of this document has been generated using LLM (Large Language Model) functionality.

— Junie

This document provides various SQL solutions for common queries against the Rick and Morty database. These examples are designed to demonstrate standard SQL patterns like JOINS, Aggregations, and filtering using the `HAVING` clause.

이 문서는 Rick and Morty 데이터베이스에 대한 일반적인 쿼리에 대한 다양한 SQL 솔루션을 제공합니다. 이 예제들은 JOINS, 집계(Aggregations), 그리고 `HAVING` 절을 사용한 필터링과 같은 표준 SQL 패턴을 보여주기 위해 설계되었습니다.

## Find characters who appeared in all specified episodes

This query finds characters that have appeared in a specific set of episodes. It uses a technique often called "Relational Division": we filter for the desired episodes, group by character, and then ensure the number of unique episodes found matches the total number of episodes in our input set.

이 쿼리는 특정 에피소드 세트에 모두 등장한 캐릭터를 찾습니다. 이는 흔히 "관계 대수 나누기(Relational Division)"라고 불리는 기술을 사용합니다: 원하는 에피소드들을 필터링하고, 캐릭터별로 그룹화한 다음, 발견된 고유 에피소드의 수가 입력된 세트의 총 에피소드 수와 일치하는지 확인합니다.

```sqlite
-- Variation 1: Starting from the character table
SELECT c.*
FROM character c
         JOIN character_episode ce ON c.id = ce.character_id
WHERE ce.episode_id IN (10, 22, 51)      -- Filter for specific episode IDs
GROUP BY c.id                            -- Group by character to aggregate their appearances
HAVING COUNT(DISTINCT ce.episode_id) = 3 -- Ensure they appear in all 3 episodes
ORDER BY c.id ASC
;
--   1  Rick Sanchez
--   2  Morty Smith
--   3  Summer Smith
--   4  Beth Smith
--   5  Jerry Smith
-- 215  Maximums Rickimus
-- 274  Quantum Rick
-- 294  Ricktiminus Sancheziminius
-- 389  Zeta Alpha Rick
```

```sqlite
-- Variation 2: Starting from the mapping table
SELECT c.*
FROM character_episode ce
         JOIN character c ON c.id = ce.character_id
WHERE ce.episode_id IN (10, 22, 51)      -- Filter for specific episode IDs
GROUP BY ce.character_id                 -- Group by character ID
HAVING COUNT(DISTINCT ce.episode_id) = 3 -- Ensure they appear in all 3 episodes
ORDER BY ce.character_id ASC
;
--   1  Rick Sanchez
--   2  Morty Smith
--   3  Summer Smith
--   4  Beth Smith
--   5  Jerry Smith
-- 215  Maximums Rickimus
-- 274  Quantum Rick
-- 294  Ricktiminus Sancheziminius
-- 389  Zeta Alpha Rick
```

## Find episodes in which all specified characters appeared together

Similar to the previous query, this finds episodes where a specific group of characters all appeared. We filter for the character IDs, group by episode, and check if the count of unique characters in that episode matches our input set size.

이전 쿼리와 마찬가지로, 이 쿼리는 특정 캐릭터 그룹이 모두 함께 등장한 에피소드를 찾습니다. 캐릭터 ID를 필터링하고, 에피소드별로 그룹화한 다음, 해당 에피소드의 고유 캐릭터 수가 입력된 세트의 크기와 일치하는지 확인합니다.

```sqlite
-- Variation 1: Joining from episode to the mapping table
SELECT e.*
FROM episode e
         JOIN character_episode ce ON e.id = ce.episode_id
WHERE ce.character_id IN (1, 2, 3, 4, 5)   -- Filter for specific character IDs
GROUP BY e.id                              -- Group by episode to count characters
HAVING COUNT(DISTINCT ce.character_id) = 5 -- Match the total number of characters (5)
ORDER BY e.id ASC
;
--  6  Rick Potion #9
--  7  Raising Gazorpazorp
--  8  Rixty Minutes
--  9  Something Ricked This Way Comes
-- 10  Close Rick-counters of the Rick Kind
-- 11  Ricksy Business
-- 12  A Rickle in Time
-- 14  Auto Erotic Assimilation
-- 15  Total Rickall
-- 16  Get Schwifty
-- 18  Big Trouble in Little Sanchez
-- 19  Interdimensional Cable 2: Tempting Fate
-- 20  Look Who's Purging Now
-- 21  The Wedding Squanchers
-- 22  The Rickshank Rickdemption
-- 23  Rickmancing the Stone
-- 26  The Whirly Dirly Conspiracy
-- 29  Morty's Mind Blowers
-- 30  The ABC's of Beth
-- 31  The Rickchurian Mortydate
-- 32  Edge of Tomorty: Rick, Die, Rickpeat
-- 33  The Old Man and the Seat
-- 35  Claw and Hoarder: Special Ricktim's Morty
-- 36  Rattlestar Ricklactica
-- 38  Promortyus
-- 39  The Vat of Acid Episode
-- 40  Childrick of Mort
-- 41  Star Mort: Rickturn of the Jerri
-- 42  Mort Dinner Rick Andre
-- 43  Mortyplicity
-- 44  A Rickconvenient Mort
-- 45  Rickdependence Spray
-- 46  Amortycan Grickfitti
-- 47  Rick & Morty's Thanksploitation Spectacular
-- 48  Gotron Jerrysis Rickvangelion
-- 49  Rickternal Friendshine of the Spotless Mort
-- 51  Rickmurai Jack
```

```sqlite
-- Variation 2: Joining from the mapping table to episode
SELECT e.*
FROM character_episode ce
         JOIN episode e ON e.id = ce.episode_id
WHERE ce.character_id IN (1, 2, 3, 4, 5)   -- Filter for characters
GROUP BY ce.episode_id                     -- Group by episode ID
HAVING COUNT(DISTINCT ce.character_id) = 5 -- Ensure all 5 characters are present
ORDER BY ce.episode_id ASC
;
--  6  Rick Potion #9
--  7  Raising Gazorpazorp
--  8  Rixty Minutes
--  9  Something Ricked This Way Comes
-- 10  Close Rick-counters of the Rick Kind
-- 11  Ricksy Business
-- 12  A Rickle in Time
-- 14  Auto Erotic Assimilation
-- 15  Total Rickall
-- 16  Get Schwifty
-- 18  Big Trouble in Little Sanchez
-- 19  Interdimensional Cable 2: Tempting Fate
-- 20  Look Who's Purging Now
-- 21  The Wedding Squanchers
-- 22  The Rickshank Rickdemption
-- 23  Rickmancing the Stone
-- 26  The Whirly Dirly Conspiracy
-- 29  Morty's Mind Blowers
-- 30  The ABC's of Beth
-- 31  The Rickchurian Mortydate
-- 32  Edge of Tomorty: Rick, Die, Rickpeat
-- 33  The Old Man and the Seat
-- 35  Claw and Hoarder: Special Ricktim's Morty
-- 36  Rattlestar Ricklactica
-- 38  Promortyus
-- 39  The Vat of Acid Episode
-- 40  Childrick of Mort
-- 41  Star Mort: Rickturn of the Jerri
-- 42  Mort Dinner Rick Andre
-- 43  Mortyplicity
-- 44  A Rickconvenient Mort
-- 45  Rickdependence Spray
-- 46  Amortycan Grickfitti
-- 47  Rick & Morty's Thanksploitation Spectacular
-- 48  Gotron Jerrysis Rickvangelion
-- 49  Rickternal Friendshine of the Spotless Mort
-- 51  Rickmurai Jack
```

## Find locations order by the number of characters who have been first seen

These queries rank locations based on how many characters originated there. We use `GROUP BY` on the location ID and `COUNT()` to aggregate the characters.

이 쿼리들은 얼마나 많은 캐릭터가 해당 장소에서 기원했는지를 기준으로 위치의 순위를 매깁니다. 위치 ID에 `GROUP BY`를 사용하고 `COUNT()`를 사용하여 캐릭터를 집계합니다.

```sqlite
-- Variation 1: Starting from location
SELECT l.*, COUNT(c.id) AS character_count
FROM location l
         JOIN character c ON l.id = c.origin_id_ -- Join on the origin location foreign key
GROUP BY l.id                                    -- Group by location to get counts per place
ORDER BY character_count DESC                    -- Order by the highest count first
;
--  20  Earth (Replacement Dimension)  155
--   1  Earth (C-137)                   33
--  96  Story Train                     29
--   6  Interdimensional Cable          16
--  78  Snake Planet                    14
-- 110  Narnia Dimension                12
--   8  Post-Apocalyptic Earth          10
--  82  Earth (Wasp Dimension)           8
-- 101  Glorzo Asteroid                  8
--   3  Citadel of Ricks                 7
```

```sqlite
-- Variation 2: Starting from character
SELECT l.*, COUNT(c.id) AS character_count
FROM character c
         JOIN location l ON c.origin_id_ = l.id -- Join with location details
GROUP BY l.id                                   -- Group by location
ORDER BY character_count DESC                   -- Order by count
;
--  20  Earth (Replacement Dimension)  155
--   1  Earth (C-137)                   33
--  96  Story Train                     29
--   6  Interdimensional Cable          16
--  78  Snake Planet                    14
-- 110  Narnia Dimension                12
--   8  Post-Apocalyptic Earth          10
--  82  Earth (Wasp Dimension)           8
-- 101  Glorzo Asteroid                  8
--   3  Citadel of Ricks                 7
```

## Find locations order by the number of characters who have been last seen

These queries rank locations based on where characters were most recently located (their current `location_id_`).

이 쿼리들은 캐릭터들이 가장 최근에 위치했던 곳(현재의 `location_id_`)을 기준으로 위치의 순위를 매깁니다.

```sqlite
-- Variation 1: Starting from location
SELECT l.*, COUNT(c.id) AS character_count
FROM location l
         JOIN character c ON l.id = c.location_id_ -- Join on current location foreign key
GROUP BY l.id                                      -- Group by location
ORDER BY character_count DESC                      -- Order by highest count
;
--  20  Earth (Replacement Dimension)  230
--   3  Citadel of Ricks               101
--   6  Interdimensional Cable          62
--   1  Earth (C-137)                   27
--  96  Story Train                     27
--  78  Snake Planet                    15
--  35  Planet Squanch                  12
--   5  Anatomy Park                    11
--  13  Nuptia 4                        11
-- 110  Narnia Dimension                11
```

```sqlite
-- Variation 2: Starting from character
SELECT l.*, COUNT(c.id) AS character_count
FROM character c
         JOIN location l ON c.location_id_ = l.id -- Join with location table
GROUP BY l.id                                     -- Group results by location
ORDER BY character_count DESC                     -- Sort by popularity
;
--  20  Earth (Replacement Dimension)  230
--   3  Citadel of Ricks               101
--   6  Interdimensional Cable          62
--   1  Earth (C-137)                   27
--  96  Story Train                     27
--  78  Snake Planet                    15
--  35  Planet Squanch                  12
--   5  Anatomy Park                    11
--  13  Nuptia 4                        11
-- 110  Narnia Dimension                11
```

