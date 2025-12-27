# SOLUTIONS (BASIC)

This document provides basic SQL solutions for common queries against the Rick and Morty database. These examples focus on simple aggregations, distribution analysis, and basic filtering techniques.

이 문서는 Rick and Morty 데이터베이스에 대한 일반적인 쿼리에 대한 기본적인 SQL 솔루션을 제공합니다. 이 예제들은 단순 집계, 분포 분석 및 기본적인 필터링 기술에 초점을 맞춥니다.

## Disclaimer

This document was authored with the assistance of Large Language Model (LLM) technology.

이 문서는 대규모 언어 모델(LLM) 기술의 도움을 받아 작성되었습니다.

## Find character distributions by status

This query provides the distributions of characters by their status (e.g., Alive, Dead, unknown).

이 쿼리는 캐릭터의 상태별(예: Alive, Dead, unknown) 분포를 제공합니다.

```sqlite
SELECT status,
       COUNT(*) AS count
FROM character
GROUP BY 1
ORDER BY count DESC
;
```

## Find character distributions by species

This query provides the distributions of characters by their species.

이 쿼리는 캐릭터의 종별 분포를 제공합니다.

```sqlite
SELECT species,
       COUNT(*) AS count
FROM character
GROUP BY 1
ORDER BY count DESC
;
```

## Find character distributions by gender

This query provides the distributions of characters by their gender.

이 쿼리는 캐릭터의 성별 분포를 제공합니다.

```sqlite
SELECT gender,
       COUNT(*) AS count
FROM character
GROUP BY 1
ORDER BY count DESC
;
```

## Find character distributions by type

This query provides the distributions of characters by their type. NULL values and empty strings are labeled as `(unknown)`.

이 쿼리는 캐릭터의 유형별 분포를 제공합니다. NULL 값과 빈 문자열은 `(unknown)`으로 표시됩니다.

```sqlite
SELECT COALESCE(NULLIF(type, ''), '(unknown)') AS type,
       COUNT(*)                                AS count
FROM character
GROUP BY 1
ORDER BY count DESC
;
```

## Find location distributions by type

This query provides the distributions of locations by their type. NULL values and empty strings are labeled as `(unknown)`.

이 쿼리는 위치의 유형별 분포를 제공합니다. NULL 값과 빈 문자열은 `(unknown)`으로 표시됩니다.

```sqlite
SELECT COALESCE(NULLIF(type, ''), '(unknown)') AS type,
       COUNT(*)                                AS count
FROM location
GROUP BY 1
ORDER BY count DESC
;
```

## Find location distributions by dimension

This query provides the distributions of locations by their dimension. NULL values and empty strings are labeled as `(unknown)`.

이 쿼리는 위치의 차원별 분포를 제공합니다. NULL 값과 빈 문자열은 `(unknown)`으로 표시됩니다.

```sqlite
SELECT COALESCE(NULLIF(dimension, ''), '(unknown)') AS dimension,
       COUNT(*)                                     AS count
FROM location
GROUP BY 1
ORDER BY count DESC
;
```

## Find characters by name pattern

This query finds characters whose names start with 'Rick'. It demonstrates the use of the `LIKE` operator for pattern matching.

이 쿼리는 이름이 'Rick'으로 시작하는 캐릭터를 찾습니다. 패턴 매칭을 위한 `LIKE` 연산자의 사용법을 보여줍니다.

```sqlite
SELECT id,
       name,
       species,
       status
FROM character
WHERE name LIKE 'Rick%'
;
```

## Find episodes by season

This query lists all episodes from the first season. It uses the `LIKE` operator to filter the `episode` code (e.g., 'S01E01').

이 쿼리는 첫 번째 시즌의 모든 에피소드를 나열합니다. `LIKE` 연산자를 사용하여 에피소드 코드(예: 'S01E01')를 필터링합니다.

```sqlite
SELECT id,
       name,
       episode
FROM episode
WHERE episode LIKE 'S01%'
;
```
