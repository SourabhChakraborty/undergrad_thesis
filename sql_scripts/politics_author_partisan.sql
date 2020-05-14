DROP TABLE IF EXISTS sc_politics_auths_partisan;
CREATE TABLE sc_politics_auths_partisan AS (
	SELECT COUNT(id) as num, author, subreddit
	FROM reddit_comments_all
	WHERE author IN (SELECT author FROM sc_politics_auths_all_2015_2016)
	AND (LOWER(subreddit)='the_donald' 
		OR LOWER(subreddit)='sandersforpresident'
		OR LOWER(subreddit)='hillaryclinton')
	AND created_utc < 1483246800
	AND created_utc >= 1420088400
	GROUP BY author, subreddit);
