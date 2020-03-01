DROP TABLE IF EXISTS relationship_advice_comments_jan_2016;
CREATE TABLE relationship_advice_comments_jan_2016 AS (
SELECT author, subreddit, body, to_timestamp(created_utc) as created_dt
FROM reddit_comments_all
WHERE subreddit = 'relationship_advice'
--Level 1 Filters: Time from January 1 2016 to February 1 2016
AND created_utc >= 1451624400
AND created_utc < 1454302800
--Level 2 Filters: Remove Known Bots
AND lower(author)  NOT LIKE '%bot%'
GROUP BY author, subreddit, body, created_dt
HAVING count(author) > 0);
--Result: 35440 entries 
