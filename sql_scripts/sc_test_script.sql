CREATE TABLE sc_test_table AS (SELECT * FROM reddit_comments_all limit 2);
\copy sc_test_table to '/home/sc2356/sc_test_table2.csv' with csv
