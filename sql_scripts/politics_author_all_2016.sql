DROP TABLE IF EXISTS sc_politics_auths_all_2015_2016;
CREATE TABLE sc_politics_auths_all_2015_2016 AS (
	WITH all_auths AS(
		SELECT author FROM sc_politics_comments_2015_2016
		GROUP BY author)
	SELECT author, random() as rand FROM all_auths
	ORDER BY rand ASC);
