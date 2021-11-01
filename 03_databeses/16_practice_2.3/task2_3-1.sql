CREATE TABLE potential_customers (
    id INTEGER NOT NULL PRIMARY KEY,
    email VARCHAR,
    name VARCHAR NOT NULL,
    surname VARCHAR NOT NULL,
    second_name VARCHAR NOT NULL,
    city VARCHAR);

COPY potential_customers FROM '/usr/src/potential_customers.csv' DELIMITER ',' CSV;

--INSERT INTO potential_customers (id, email, name, surname, second_name, city) VALUES
--	(1, 'user1@gmail.com', 'name1', 'surname1', 'second_name1', 'city1'),
--	(2, 'user1@gmail.com', 'name2', 'surname2', 'second_name2', 'city5'),
--	(3, 'user3@gmail.com', 'name3', 'surname3', 'second_name3', 'city17'),
--	(4, 'user1@gmail.com', 'name4', 'surname2', 'second_name2', 'city5'),
--	(5, 'user4@gmail.com', 'name5', 'surname4', 'second_name4', 'city17'),
--	(6, 'user1@gmail.com', 'name2.1', 'surname2', 'second_name2', 'city1'),
--	(7, 'user4@gmail.com', 'name3.8', 'surname4', 'second_name4', 'city15');

SELECT name, email FROM potential_customers WHERE "city"='city17';

