# SOLUTIONS (ADVANCED)

This document provides advanced SQL solutions for common queries against the Rick and Morty database. These examples demonstrate complex patterns such as Relational Division, Window Functions, and Self-Joins to extract deep insights.

이 문서는 Rick and Morty 데이터베이스에 대한 일반적인 쿼리에 대한 고급 SQL 솔루션을 제공합니다. 이 예제들은 심층적인 통찰력을 추출하기 위해 관계 대수 나누기(Relational Division), 윈도우 함수(Window Functions), 셀프 조인(Self-Joins)과 같은 복잡한 패턴을 보여줍니다.

## Disclaimer

This document was authored with the assistance of Large Language Model (LLM) technology.

이 문서는 대규모 언어 모델(LLM) 기술의 도움을 받아 작성되었습니다.

## Find characters who appeared in all specified episodes

This query finds characters that have appeared in a specific set of episodes. It uses a technique often called "Relational Division": we filter for the desired episodes, group by character, and then ensure the number of unique episodes found matches the total number of episodes in our input set (3 in this case).

이 쿼리는 특정 에피소드 세트에 모두 등장한 캐릭터를 찾습니다. 이는 흔히 "관계 대수 나누기(Relational Division)"라고 불리는 기술을 사용합니다: 원하는 에피소드들을 필터링하고, 캐릭터별로 그룹화한 다음, 발견된 고유 에피소드의 수가 입력된 세트의 총 에피소드 수(이 경우 3개)와 일치하는지 확인합니다.

### Variation 1: Starting from the character table

```sqlite
SELECT c.id, c.name
FROM character c
         JOIN character_episode ce ON c.id = ce.character_id
WHERE ce.episode_id IN (10, 22, 51)
GROUP BY c.id
HAVING COUNT(DISTINCT ce.episode_id) = 3
ORDER BY c.id ASC
;
```

### Variation 2: Starting from the mapping table

```sqlite
SELECT c.id, c.name
FROM character_episode ce
         JOIN character c ON c.id = ce.character_id
WHERE ce.episode_id IN (10, 22, 51)
GROUP BY ce.character_id
HAVING COUNT(DISTINCT ce.episode_id) = 3
ORDER BY ce.character_id ASC
;
```

## Find episodes in which all specified characters appeared together

Similar to the previous query, this finds episodes where a specific group of characters all appeared together. We filter for the character IDs, group by episode, and check if the count of unique characters in that episode matches our input set size (5 in this case).

이전 쿼리와 마찬가지로, 이 쿼리는 특정 캐릭터 그룹이 모두 함께 등장한 에피소드를 찾습니다. 캐릭터 ID를 필터링하고, 에피소드별로 그룹화한 다음, 해당 에피소드의 고유 캐릭터 수가 입력된 세트의 크기(이 경우 5명)와 일치하는지 확인합니다.

### Variation 1: Joining from episode to the mapping table

```sqlite
SELECT e.id, e.name, e.episode
FROM episode e
         JOIN character_episode ce ON e.id = ce.episode_id
WHERE ce.character_id IN (1, 2, 3, 4, 5)
GROUP BY e.id
HAVING COUNT(DISTINCT ce.character_id) = 5
ORDER BY e.id ASC
;
```

### Variation 2: Joining from the mapping table to episode

```sqlite
SELECT e.id, e.name, e.episode
FROM character_episode ce
         JOIN episode e ON e.id = ce.episode_id
WHERE ce.character_id IN (1, 2, 3, 4, 5)
GROUP BY ce.episode_id
HAVING COUNT(DISTINCT ce.character_id) = 5
ORDER BY ce.episode_id ASC
;
```

## Rank characters by episode count within each species

This query uses a Window Function (`RANK()`) to rank characters within each species based on the number of episodes they appeared in. This is useful for identifying "main" characters for each biological group.

이 쿼리는 윈도우 함수(`RANK()`)를 사용하여 각 종(species) 내에서 출연한 에피소드 수를 기준으로 캐릭터의 순위를 매깁니다. 이는 각 생물학적 그룹의 "주요" 캐릭터를 식별하는 데 유용합니다.

```sqlite
WITH character_counts AS (
    SELECT c.id,
           c.name,
           c.species,
           COUNT(ce.episode_id) AS episode_count
    FROM character c
             JOIN character_episode ce ON c.id = ce.character_id
    GROUP BY c.id
)
SELECT id,
       name,
       species,
       episode_count,
       RANK() OVER (PARTITION BY species ORDER BY episode_count DESC) AS rank
FROM character_counts
ORDER BY species ASC, rank ASC
;
```

## Find character pairs that appeared together in the most episodes

This query uses a self-join on the `character_episode` table to find pairs of characters that have shared the most screen time (appeared in the same episodes).

이 쿼리는 `character_episode` 테이블의 셀프 조인(self-join)을 사용하여 가장 많은 에피소드에 함께 출연한 캐릭터 쌍을 찾습니다.

```sqlite
SELECT c1.name AS character_1,
       c2.name AS character_2,
       COUNT(*) AS shared_episodes
FROM character_episode ce1
         JOIN character_episode ce2 ON ce1.episode_id = ce2.episode_id AND ce1.character_id < ce2.character_id
         JOIN character c1 ON ce1.character_id = c1.id
         JOIN character c2 ON ce2.character_id = c2.id
GROUP BY ce1.character_id, ce2.character_id
ORDER BY shared_episodes DESC
;
```

## Find episodes with the highest species diversity

This query identifies episodes with the highest number of distinct species, demonstrating complex aggregation across three joined tables.

이 쿼리는 세 개의 조인된 테이블에 걸친 복잡한 집계를 통해 가장 다양한 종(species)이 등장한 에피소드를 식별합니다.

```sqlite
SELECT e.id,
       e.name,
       e.episode,
       COUNT(DISTINCT c.species) AS species_count
FROM episode e
         JOIN character_episode ce ON e.id = ce.episode_id
         JOIN character c ON ce.character_id = c.id
GROUP BY e.id
ORDER BY species_count DESC, e.id ASC
;
```

## Find the most recently created character for each species

This query uses the `ROW_NUMBER()` window function to identify the single most recently created character within each species group.

이 쿼리는 `ROW_NUMBER()` 윈도우 함수를 사용하여 각 종(species) 그룹 내에서 가장 최근에 생성된 캐릭터를 하나씩 식별합니다.

```sqlite
SELECT id,
       name,
       species,
       created
FROM (
    SELECT id,
           name,
           species,
           created,
           ROW_NUMBER() OVER (PARTITION BY species ORDER BY created DESC) AS rn
    FROM character
)
WHERE rn = 1
ORDER BY species ASC
;
```

## Find characters who appeared in all seasons

This query identifies characters who have appeared in at least one episode of every season. It uses a `HAVING` clause to compare the number of distinct seasons for each character with the total number of distinct seasons in the database.

이 쿼리는 모든 시즌의 에피소드에 최소 한 번 이상 출연한 캐릭터를 식별합니다. `HAVING` 절을 사용하여 각 캐릭터의 고유 시즌 수와 데이터베이스에 있는 총 고유 시즌 수를 비교합니다.

```sqlite
SELECT c.id,
       c.name
FROM character c
         JOIN character_episode ce ON c.id = ce.character_id
         JOIN episode e ON ce.episode_id = e.id
GROUP BY c.id
HAVING COUNT(DISTINCT SUBSTR(e.episode, 1, 3)) = (
    SELECT COUNT(DISTINCT SUBSTR(episode, 1, 3))
    FROM episode
)
ORDER BY c.id ASC
;
```
