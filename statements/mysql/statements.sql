CREATE DATABASE "shop";

CREATE USER 'shop'@'localhost';
GRANT ALL PRIVILEGES ON shop.* to 'shop'@'localhost';

CREATE USER 'viewer'@'localhost';
GRANT SELECT ON shop.* to 'viewer'@'localhost';

CREATE TABLE shop.category (
    category_title varchar(50)
);

INSERT INTO shop.category(category_title) VALUES
    ('category_1'),
    ('category_2'),
    ('category_3');
    
CREATE TABLE shop.article(
    article_title varchar(50),
    article_category varchar(50),
    article_price real
);

INSERT INTO shop.article(article_title, article_category, article_price) VALUES
    ('article_title_1', 'article_category', 1.00),
    ('article_title_2', 'article_category', 1.00),
    ('article_title_3', 'article_category', 1.00);
    
UPDATE shop.article
SET article_price = 3.50
WHERE article_title = 'article_title_1';

UPDATE shop.article
SET article_price = 1.1 * article_price;

DELETE FROM shop.article
WHERE article_title = 'article_title_2';

SELECT * FROM shop.article
ORDER BY article_price DESC;

SELECT * FROM shop.article
ORDER BY article_price;


SELECT * FROM shop.article
ORDER BY article_price DESC
LIMIT 3
OFFSET 3;

SELECT article_title FROM (
    SELECT * FROM shop.article
    ORDER BY article_price
    LIMIT 1
) AS first_row;

SELECT article_title FROM (
    SELECT * FROM shop.article
    ORDER BY article_price DESC
    LIMIT 1
) AS first_row;

SELECT COUNT(*) FROM shop.article;

SELECT AVG(article_price) FROM shop.article;

CREATE VIEW shop.top_articles AS
SELECT * FROM shop.article
ORDER BY article_price DESC
LIMIT 3;