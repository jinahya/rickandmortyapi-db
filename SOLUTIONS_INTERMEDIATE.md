# SOLUTIONS (INTERMEDIATE)

This document provides intermediate SQL solutions for common queries against the Rick and Morty database. These examples demonstrate standard SQL patterns like `JOIN`s, multi-table aggregations, and filtering based on related data.

이 문서는 Rick and Morty 데이터베이스에 대한 일반적인 쿼리에 대한 중급 SQL 솔루션을 제공합니다. 이 예제들은 `JOIN`, 다중 테이블 집계, 연관된 데이터를 기반으로 한 필터링과 같은 표준 SQL 패턴을 보여줍니다.

## Disclaimer

This document was authored with the assistance of Large Language Model (LLM) technology.

이 문서는 대규모 언어 모델(LLM) 기술의 도움을 받아 작성되었습니다.

## Find locations ordered by the number of characters who have been first seen

These queries rank locations based on how many characters originated there (first seen). We use `GROUP BY` on the location ID and `COUNT()` to aggregate the characters.

이 쿼리들은 얼마나 많은 캐릭터가 해당 장소에서 기원했는지(처음 발견됨)를 기준으로 위치의 순위를 매깁니다. 위치 ID에 `GROUP BY`를 사용하고 `COUNT()`를 사용하여 캐릭터를 집계합니다.

### Variation 1: Starting from location

```sqlite
SELECT l.id,
       l.name,
       COUNT(c.id) AS character_count
FROM location l
         JOIN character c ON l.id = c.origin_id_
GROUP BY l.id
ORDER BY character_count DESC
;
```

### Variation 2: Starting from character

```sqlite
SELECT l.id,
       l.name,
       COUNT(c.id) AS character_count
FROM character c
         JOIN location l ON c.origin_id_ = l.id
GROUP BY l.id
ORDER BY character_count DESC
;
```

## Find locations ordered by the number of characters who have been last seen

These queries rank locations based on where characters were most recently located (their current `location_id_`).

이 쿼리들은 캐릭터들이 가장 최근에 위치했던 곳(현재의 `location_id_`)을 기준으로 위치의 순위를 매깁니다.

### Variation 1: Starting from location

```sqlite
SELECT l.id,
       l.name,
       COUNT(c.id) AS character_count
FROM location l
         JOIN character c ON l.id = c.location_id_
GROUP BY l.id
ORDER BY character_count DESC
;
```

### Variation 2: Starting from character

```sqlite
SELECT l.id,
       l.name,
       COUNT(c.id) AS character_count
FROM character c
         JOIN location l ON c.location_id_ = l.id
GROUP BY l.id
ORDER BY character_count DESC
;
```

## Find characters with the number of episodes they appeared in

This query counts how many episodes each character has appeared in by joining the `character` and `character_episode` tables.

이 쿼리는 `character`와 `character_episode` 테이블을 조인하여 각 캐릭터가 몇 개의 에피소드에 출연했는지 계산합니다.

```sqlite
SELECT c.id,
       c.name,
       COUNT(ce.episode_id) AS episode_count
FROM character c
         JOIN character_episode ce ON c.id = ce.character_id
GROUP BY c.id
ORDER BY episode_count DESC
;
```

## Find episodes with the number of characters who appeared in them

This query counts the number of characters in each episode by joining the `episode` and `character_episode` tables.

이 쿼리는 `episode`와 `character_episode` 테이블을 조인하여 각 에피소드에 출연한 캐릭터 수를 계산합니다.

```sqlite
SELECT e.id,
       e.name,
       e.episode,
       COUNT(ce.character_id) AS character_count
FROM episode e
         JOIN character_episode ce ON e.id = ce.episode_id
GROUP BY e.id
ORDER BY character_count DESC, e.id ASC
;
```

## Find characters whose current location is different from their origin

This query identifies characters who are currently located in a place other than where they originated. It filters out characters with unknown origin or current location.

이 쿼리는 현재 위치가 태어난 곳과 다른 캐릭터들을 찾습니다. 출신지나 현재 위치가 알 수 없는 경우(unknown)는 제외합니다.

```sqlite
SELECT c.id,
       c.name,
       lo.name AS origin_name,
       ll.name AS current_location_name
FROM character c
         JOIN location lo ON c.origin_id_ = lo.id
         JOIN location ll ON c.location_id_ = ll.id
WHERE c.origin_id_ != c.location_id_
;
```

## Find locations with their resident counts

This query provides a list of locations along with the number of residents associated with each, using the `location_resident` table.

이 쿼리는 `location_resident` 테이블을 사용하여 각 장소와 해당 장소에 거주하는 주민 수를 나열합니다.

```sqlite
SELECT l.id,
       l.name,
       COUNT(lr.resident_id) AS resident_count
FROM location l
         JOIN location_resident lr ON l.id = lr.location_id
GROUP BY l.id
ORDER BY resident_count DESC
;
```

## Find characters who appeared in a specific episode

This query finds all characters who appeared in the episode named 'Pilot'. It demonstrates joining the `character`, `character_episode`, and `episode` tables.

이 쿼리는 'Pilot'이라는 이름의 에피소드에 출연한 모든 캐릭터를 찾습니다. `character`, `character_episode`, `episode` 테이블을 조인하는 방법을 보여줍니다.

```sqlite
SELECT c.id,
       c.name,
       e.name AS episode_name
FROM character c
         JOIN character_episode ce ON c.id = ce.character_id
         JOIN episode e ON ce.episode_id = e.id
WHERE e.name = 'Pilot'
;
```

## Find total residents per location type

This query calculates the total number of residents for each location type. It joins the `location` and `location_resident` tables and aggregates the results by type.

이 쿼리는 각 위치 유형별 총 거주자 수를 계산합니다. `location`과 `location_resident` 테이블을 조인하고 유형별로 결과를 집계합니다.

```sqlite
SELECT l.type,
       COUNT(lr.resident_id) AS total_residents
FROM location l
         JOIN location_resident lr ON l.id = lr.location_id
GROUP BY l.type
ORDER BY total_residents DESC
;
```
