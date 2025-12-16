--


-- --------------------------------------------------------------------------------------------------------- location_id
SELECT lr.location_id, l.id
FROM location_resident lr
         LEFT OUTER JOIN location l ON lr.location_id = l.id
WHERE l.id IS NULL
;

-- --------------------------------------------------------------------------------------------------------- resident_id
SELECT lr.*, c.id
FROM location_resident lr
         LEFT OUTER JOIN character c ON lr.resident_id = c.id
WHERE c.id IS NULL
;

-- location/{id}/$.residents = /character/{id}$.location.id
SELECT lr.*, c.id
FROM location_resident lr
         LEFT OUTER JOIN character c ON lr.resident_id = c.id
WHERE c.id IS NOT NULL
  AND c.location_id_ <> lr.location_id
;


SELECT lr.*, c.id, c.location_id_
FROM location_resident lr
         LEFT OUTER JOIN character c ON lr.resident_id = c.id
WHERE c.id IS NULL
;

SELECT resident_id, COUNT(1)
FROM location_resident
GROUP BY resident_id
-- HAVING COUNT(1) > 1
-- ORDER BY COUNT(1)
;