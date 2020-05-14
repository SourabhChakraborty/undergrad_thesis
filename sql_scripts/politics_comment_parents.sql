DROP TABLE IF EXISTS sc_politics_parent_comments;
CREATE TABLE sc_politics_parent_comments AS (
SELECT author, subreddit, body, id, score, created_utc, link_id, parent_id
FROM reddit_comments_all
WHERE id IN (SELECT id FROM sc_derived_parent_ids));
