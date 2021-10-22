CREATE TABLE order_status (order_status_id INTEGER NOT NULL PRIMARY KEY, status_name VARCHAR(255) NOT NULL);
CREATE TABLE "order" (order_id INTEGER NOT NULL PRIMARY KEY,
	carts_cart_id INTEGER NOT NULL,
	order_status_order_status_id INTEGER,
	shipping_total DECIMAL,
	total DECIMAL,
	created_at TIMESTAMP(2),
	updated_at TIMESTAMP(2));
CREATE TABLE carts (cart_id INTEGER NOT NULL PRIMARY KEY,
	users_user_id INTEGER,
	subtotal DECIMAL,
	total DECIMAL,
	timestamp TIMESTAMP(2));
CREATE TABLE users (user_id INTEGER NOT NULL PRIMARY KEY,
	email VARCHAR(255),
	password VARCHAR(255),
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	middle_name VARCHAR(255),
	if_staff SMALLINT,
	country VARCHAR(255),
	city VARCHAR(255),
	address TEXT);
CREATE TABLE cart_product (carts_cart_id INTEGER, products_product_id INTEGER);
CREATE TABLE products (product_id INTEGER PRIMARY KEY NOT NULL,
	product_title VARCHAR(255),
	product_description TEXT,
	in_stock INTEGER,
	price FLOAT,
	slug VARCHAR(45),
	category_id INTEGER);
CREATE TABLE categories (category_id INTEGER PRIMARY KEY NOT NULL,
	category_title VARCHAR(255),
	category_description TEXT);
ALTER TABLE "order" ADD CONSTRAINT carts_cart_id_fk FOREIGN KEY (carts_cart_id) REFERENCES carts (cart_id);
ALTER TABLE "order" ADD CONSTRAINT order_status_order_status_id_fk FOREIGN KEY (order_status_order_status_id) REFERENCES Order_status (order_status_id);
ALTER TABLE carts ADD CONSTRAINT users_user_id_fk FOREIGN KEY (users_user_id) REFERENCES users (user_id);
ALTER TABLE cart_product ADD CONSTRAINT cart_product_cart_id_fk FOREIGN KEY (carts_cart_id) REFERENCES carts (cart_id);
ALTER TABLE cart_product ADD CONSTRAINT products_product_id_fk FOREIGN KEY (products_product_id) REFERENCES products (product_id);
ALTER TABLE products ADD CONSTRAINT products_category_id_fk FOREIGN KEY (category_id) REFERENCES Categories (category_id);