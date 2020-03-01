DROP TABLE IF EXISTS sc_politics_auth_comments;
CREATE TABLE sc_politics_auth_comments AS (
SELECT author, subreddit, body, score, created_utc, link_id, parent_id
FROM reddit_comments_all
WHERE author IN (SELECT author FROM sc_politics_auths)
AND created_utc < 1464753600);
