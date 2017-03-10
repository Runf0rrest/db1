CREATE SCHEMA "shop";

CREATE USER "shop";
GRANT ALL PRIVILEGES ON DATABASE "shop" TO "shop";

CREATE USER "viewer";
GRANT SELECT ON ALL TABLES IN SCHEMA "shop" TO "viewer";

CREATE TABLE "category" (
    category_title VARCHAR(50)
    );

INSERT INTO "category" (category_title) VALUES
    ('title1'),
    ('title2'),
    ('title3');

CREATE TABLE "article" (
    article_title VARCHAR(50),
    article_category VARCHAR(50),
    article_price REAL
    );

INSERT INTO "article" (article_title, article_category, article_price VALUES
    ('article_1', 'category_1', 1.0),
    ('article_2', 'category_2', 1.0),
    ('article_3', 'category_3', 1.0)
);

INSERT INTO "article" VALUES
    ('article_1', 'category_1', 1.0),
    ('article_2', 'category_2', 1.0),
    ('article_3', 'category_3', 1.0);
    
UPDATE "article"
SET article_price = 3.50
WHERE article_title = 'article_1';

UPDATE "article"
SET article_price = 1.1 * article_price;

DELETE FROM "article"
WHERE "article_title" = 'article_2';

SELECT * FROM "article"
ORDER BY "article_title";

SELECT * FROM "article"
ORDER BY "article_price" DESC;

SELECT * FROM "article"
ORDER BY "article_price" DESC
LIMIT 3;

SELECT * FROM "article"
ORDER BY "article_price"
LIMIT 3;

SELECT * FROM "article"
ORDER BY "article_price" DESC
LIMIT 3
OFFSET 3;

SELECT "article_title" FROM (
    SELECT * FROM "article"
    ORDER BY "article_price" DESC
    LIMIT 1
) AS "title";


SELECT "article_title" FROM (
    SELECT * FROM "article"
    ORDER BY "article_price"
    LIMIT 1
) AS "title";

SELECT COUNT(*) FROM "article";

SELECT AVG("article_price") FROM "article";

CREATE VIEW "top_articles" AS
SELECT * FROM "article"
ORDER BY "article_price" DESC
LIMIT 3;

