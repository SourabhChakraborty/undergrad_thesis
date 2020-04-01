DROP TABLE IF EXISTS politics_sample3;
CREATE TABLE politics_sample3 AS (
SELECT *, random() AS rand
FROM sc_politics_comments_2015_2016j  
ORDER BY rand ASC
LIMIT 1000000);
