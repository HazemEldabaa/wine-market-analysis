SELECT * 
FROM wines
ORDER BY ratings_average DESC
LIMIT 20

SELECT * 
FROM countries


SELECT wines.name as winery_name, wines.ratings_average AS avg_ratings, vintages.name AS wine_name
FROM wines
join vintages on vintages.wine_id = wines.id


SELECT
    wines.name AS winery_name,
    wines.ratings_average AS avg_ratings,
    wines.ratings_count AS ratings_count,
    wines.id,
    CASE
        WHEN INSTR(vintages.name, wines.name) > 0 THEN
            TRIM(SUBSTR(vintages.name, 1, INSTR(vintages.name, wines.name) - 1))
        ELSE
            vintages.name
    END AS wine_name_cleaned
FROM
    wines
JOIN vintages ON vintages.wine_id = wines.id
GROUP BY wine_name_cleaned
ORDER BY avg_ratings DESC

SELECT *
FROM most_used_grapes_per_country
GROUP BY grape_id

SELECT *
FROM keywords_wine
JOIN WineDetails on WineDetails.id = wine_id
join keywords on keywords.id = keyword_id
WHERE keywords.name IN ('coffee', 'toast', 'green apple', 'cream', 'citrus') AND count >= 10
