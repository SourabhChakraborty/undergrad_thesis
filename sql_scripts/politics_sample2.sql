DROP TABLE IF EXISTS politics_sample1;
CREATE TABLE politics_sample2 AS (
SELECT *, random() AS rand
FROM sc_politics_comments_2015_2016j  
ORDER BY rand ASC
LIMIT 10000);
