DROP TABLE IF EXISTS sc_politics_auth_comments2;
CREATE TABLE sc_politics_auth_comments2 AS (
SELECT author, subreddit, body, score, created_utc, link_id, parent_id
FROM reddit_comments_all
WHERE author IN (SELECT author FROM sc_politics_auths2)
AND created_utc < 1464753600);
