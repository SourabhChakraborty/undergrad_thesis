DROP TABLE IF EXISTS sc_politics_auths2;
CREATE TABLE sc_politics_auths2 AS (
	SELECT author FROM sc_politics_auths_all
	LIMIT 20000);
