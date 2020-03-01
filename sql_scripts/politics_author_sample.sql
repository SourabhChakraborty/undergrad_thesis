DROP TABLE IF EXISTS sc_politics_auths;
CREATE TABLE sc_politics_auths AS (
	WITH all_auths AS(
		SELECT author FROM sc_politics_comments_2015_2016j
		GROUP BY author)
	SELECT author, random() as rand FROM all_auths
	ORDER BY rand ASC
	LIMIT 2000);
