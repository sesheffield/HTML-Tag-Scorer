Create table MySQL statement

CREATE TABLE IF NOT EXISTS markupProject (
name VARCHAR(255) NOT NULL, 
score INT NOT NULL,
date date NOT NULL,
UNIQUE KEY (name, date));

Query to find the average score across each key statement

SELECT name, score FROM markupProject WHERE name = unique_id;
