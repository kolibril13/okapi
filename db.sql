-- CREATE TABLE IF NOT EXISTS users (
-- user_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
-- username varchar(50) NOT NULL UNIQUE,
-- email varchar(255) NOT NULL UNIQUE
-- );

-- ALTER TABLE users 
-- ADD COLUMN name varchar(30) NOT NULL;

-- DROP TABLE users;


-- INSERT INTO users (username, email, name) 
-- VALUES ('Calcur', 'hello@email.com' , 'Csdssd');

-- UPDATE users
-- SET name = 'J S'
-- WHERE user_id = 1;

DELETE FROM users
WHERE user_id = 1;

SELECT * FROM users;

-- psql -h localhost -d postgres

-- \dt

-- \i db.sql 