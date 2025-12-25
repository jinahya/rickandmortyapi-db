# Solutions

## Find characters who appeared in all specified episodes

```sqlite
SELECT c.*
FROM character c
         JOIN character_episode ce ON c.id = ce.character_id
WHERE ce.episode_id IN (10, 22, 51)
GROUP BY c.id
HAVING COUNT(DISTINCT ce.episode_id) = 3
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
SELECT c.*
FROM character_episode ce
         JOIN character c ON c.id = ce.character_id
WHERE ce.episode_id IN (10, 22, 51)
GROUP BY ce.character_id
HAVING COUNT(DISTINCT ce.episode_id) = 3
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

```sqlite
SELECT e.*
FROM episode e
         JOIN character_episode ce ON e.id = ce.episode_id
WHERE ce.character_id IN (1, 2, 3, 4, 5)
GROUP BY e.id
HAVING COUNT(DISTINCT ce.character_id) = 5
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
SELECT e.*
FROM character_episode ce
         JOIN episode e ON e.id = ce.episode_id
WHERE ce.character_id IN (1, 2, 3, 4, 5)
GROUP BY ce.episode_id
HAVING COUNT(DISTINCT ce.character_id) = 5
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

```sqlite
SELECT l.*, COUNT(c.id) AS character_count
FROM location l
         JOIN character c ON l.id = c.origin_id_
GROUP BY l.id
ORDER BY character_count DESC
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
SELECT l.*, COUNT(c.id) AS character_count
FROM character c
         JOIN location l ON c.origin_id_ = l.id
GROUP BY l.id
ORDER BY character_count DESC
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

```sqlite
SELECT l.*, COUNT(c.id) AS character_count
FROM location l
         JOIN character c ON l.id = c.location_id_
GROUP BY l.id
ORDER BY character_count DESC
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
SELECT l.*, COUNT(c.id) AS character_count
FROM character c
         JOIN location l ON c.location_id_ = l.id
GROUP BY l.id
ORDER BY character_count DESC
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

