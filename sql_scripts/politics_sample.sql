DROP TABLE IF EXISTS politics_sample1;
CREATE TABLE politics_sample1 AS (
SELECT *, random() AS rand
FROM politics_comments_2015_2016 
WHERE created_dt < to_timestamp(1464753600) 
ORDER BY rand ASC
LIMIT 10000);
