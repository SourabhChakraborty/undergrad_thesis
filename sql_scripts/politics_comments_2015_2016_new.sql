DROP TABLE IF EXISTS sc_politics_comments_2015_2016_2;
CREATE TABLE sc_politics_comments_2015_2016_2 AS (
SELECT author, subreddit, body, score, to_timestamp(created_utc) as created_dt, link_id, parent_id, id
FROM reddit_comments_all
WHERE subreddit = 'politics'
--Level 1 Filters: Time from January 1 2015 to January 1 2017
AND created_utc >= 1420131600
AND created_utc < 1483246800
--Level 2 Filters: Remove Known Bots
AND lower(author)  NOT LIKE '%bot%'
AND lower(author) NOT IN (SELECT lower(author) FROM botlist_chenhao)
AND lower(author) NOT IN (SELECT lower(author) FROM botlist_goodbot_badbot)
AND lower(author) NOT IN (SELECT lower(author) FROM russianlist_reddit));
--Result: 10429145 entries 
