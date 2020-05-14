DROP TABLE IF EXISTS sc_politics_auths_partisan2;
CREATE TABLE sc_politics_auths_partisan2 AS (
-- Convert groups to The_Donald, SandersForPresident, and HillaryClinton counts
	WITH td_count AS (
		SELECT author, num AS td_num FROM sc_politics_auths_partisan
		WHERE LOWER(subreddit)='the_donald'
	),

	sfp_count AS (
		SELECT author, num AS sfp_num FROM sc_politics_auths_partisan
                WHERE LOWER(subreddit)='sandersforpresident'
	),

	hc_count AS(
	SELECT author, num AS hc_num FROM sc_politics_auths_partisan
                WHERE LOWER(subreddit)='hillaryclinton'
	)
 
-- Join on all authors
	SELECT sc_politics_auths_all_2015_2016.author AS author, COALESCE(td_count.td_num,0) AS td_num, COALESCE(sfp_count.sfp_num,0) AS sfp_num, COALESCE(hc_count.hc_num,0) AS hc_num 
	FROM sc_politics_auths_all_2015_2016
	LEFT JOIN td_count ON sc_politics_auths_all_2015_2016.author = td_count.author
	LEFT JOIN sfp_count ON sc_politics_auths_all_2015_2016.author = sfp_count.author
	LEFT JOIN hc_count ON sc_politics_auths_all_2015_2016.author = hc_count.author);
