--Pull all authors who qualify for our respective filters
DROP TABLE IF EXISTS arproj_seq_authors_all;
CREATE TABLE arproj_seq_authors_all AS (

    --Get authors who posted in the time frame
    WITH authors_in_tf AS
        (SELECT author
        FROM reddit_comments_all
        --Level 1 Filter: In Time Frame
        WHERE created_utc >= 1454302800
         AND created_utc < 1464753600
         --Level 2 Filters: Remove Known Bots
         AND lower(author)  NOT LIKE '%bot%'
         AND lower(author) NOT IN (SELECT lower(author) FROM botlist_chenhao)
         AND lower(author) NOT IN (SELECT lower(author) FROM botlist_goodbot_badbot)
         AND lower(author) NOT IN (SELECT lower(author) FROM russianlist_reddit)
        GROUP BY author
        --Remove authors who do not have any posts in the time frmae
        HAVING count(author) > 0)

    --Level 3 Filter: Get authors who did not post in the time frame
    SELECT author
    FROM reddit_comments_all
    WHERE author IN (SELECT * FROM authors_in_tf)
     AND created_utc < 1422766800
    GROUP BY author
    HAVING count(author) > 0);


--Add metadata (aka, how many posts they made to td, sfp, or neither before and during the time frame)
DROP TABLE IF EXISTS arproj_seq_authors_all_meta;
CREATE TABLE arproj_seq_authors_all_meta AS (
    SELECT author,
            sum(td_post_pre) AS td_posts_pre,
            sum(td_post_tf) AS td_posts_tf,
            sum(sfp_post_pre) AS sfp_posts_pre,
            sum(sfp_post_tf) AS sfp_posts_tf,
            sum(total_post_pre) AS total_posts_pre,
            sum(total_post_tf) AS total_posts_tf,
            count(author) AS total_posts
    FROM 
        (SELECT author,
            (CASE WHEN (subreddit = 'The_Donald' AND created_utc < 1454302800) THEN 1 ELSE 0 END) AS td_post_pre,
            (CASE WHEN (subreddit = 'The_Donald' AND created_utc >= 1454302800 AND created_utc < 1464753600) THEN 1 ELSE 0 END) AS td_post_tf,
            (CASE WHEN (subreddit = 'SandersForPresident' AND created_utc < 1454302800) THEN 1 ELSE 0 END) AS sfp_post_pre,
            (CASE WHEN (subreddit = 'SandersForPresident' AND created_utc >= 1454302800 AND created_utc < 1464753600) THEN 1 ELSE 0 END) AS sfp_post_tf,
            (CASE WHEN (created_utc < 1454302800) THEN 1 ELSE 0 END) AS total_post_pre,
            (CASE WHEN (created_utc >= 1454302800 AND created_utc < 1464753600) THEN 1 ELSE 0 END) AS total_post_tf
        FROM reddit_comments_all
        WHERE author IN (SELECT author FROM arproj_seq_authors_all)) AS conf_data
    GROUP BY author);

         
--Pull 1000 people and their posts, and check if those posts are in political subreddits
DROP TABLE IF EXISTS arproj_td_sample;
CREATE TABLE arproj_td_sample AS (
    
    --Sample 1000 authors
    WITH td_sample AS (
        SELECT author
        FROM (
            SELECT author, random() AS rand
            FROM arproj_seq_authors_all_meta
            WHERE td_posts_pre = 0
             AND td_posts_tf > 0
             AND sfp_posts_pre = 0
             AND sfp_posts_tf = 0) AS all_td_authors
        ORDER BY rand ASC
        LIMIT 1000),

    --Get lists of subreddits to check if a subreddit is political, populist, left leaning, or right leaning
    pol_subs AS
        (SELECT subreddit
         FROM political_subs),

    pop_subs AS 
        (SELECT subreddit
         FROM political_subs
         WHERE RIGHT(partisan_lean,8) = 'Populist'),

    leftwing_subs AS 
        (SELECT subreddit
         FROM political_subs
         WHERE LEFT(partisan_lean,4) = 'Left'),

    rightwing_subs AS 
        (SELECT subreddit
         FROM political_subs
         WHERE LEFT(partisan_lean,5) = 'Right')


    SELECT author, subreddit, body, to_timestamp(created_utc) as created_dt,
        (CASE WHEN subreddit IN (SELECT * FROM pol_subs) THEN 1 ELSE 0 END) AS political_sub,
        (CASE WHEN subreddit IN (SELECT * FROM pop_subs) THEN 1 ELSE 0 END) AS populist_sub,
        (CASE WHEN subreddit IN (SELECT * FROM leftwing_subs) THEN 1
              WHEN subreddit IN (SELECT * FROM rightwing_subs) THEN -1
              ELSE 0 END) AS political_sub_direction
    FROM reddit_comments_all
    WHERE author IN (SELECT * FROM td_sample)
     AND created_utc < 1464753600);