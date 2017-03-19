
CREATE TABLE "article" (
    article_id SERIAL PRIMARY KEY,
    article_created INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER),
	article_title varchar(50),
	article_text text,
    article_updated INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER)
);

CREATE OR REPLACE FUNCTION update_article_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.article_updated = cast(extract(epoch from now()) AS INTEGER);
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER "article_update"
BEFORE UPDATE
ON article
FOR EACH ROW
EXECUTE PROCEDURE update_article_timestamp();

CREATE TABLE "category" (
    category_id SERIAL PRIMARY KEY,
    category_created INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER),
	category_title varchar(50),
    category_updated INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER)
);

CREATE OR REPLACE FUNCTION update_category_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.category_updated = cast(extract(epoch from now()) AS INTEGER);
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER "category_update"
BEFORE UPDATE
ON category
FOR EACH ROW
EXECUTE PROCEDURE update_category_timestamp();

CREATE TABLE "tag" (
    tag_id SERIAL PRIMARY KEY,
    tag_created INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER),
	tag_value varchar(50),
    tag_updated INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER)
);

CREATE OR REPLACE FUNCTION update_tag_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.tag_updated = cast(extract(epoch from now()) AS INTEGER);
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER "tag_update"
BEFORE UPDATE
ON tag
FOR EACH ROW
EXECUTE PROCEDURE update_tag_timestamp();

ALTER TABLE "article"
ADD COLUMN category_id INTEGER REFERENCES category(category_id);

CREATE TABLE "article_tag" (
    article_id INTEGER REFERENCES article(article_id),
    tag_id INTEGER REFERENCES tag(tag_id)
);
