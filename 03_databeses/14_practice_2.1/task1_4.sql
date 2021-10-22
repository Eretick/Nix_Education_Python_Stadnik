COPY users FROM '/usr/src/task-data/users.csv' DELIMITER ',' CSV;
COPY carts FROM '/usr/src/task-data/carts.csv' DELIMITER ',' CSV;
COPY order_status FROM '/usr/src/task-data/order_statuses.csv' DELIMITER ',' CSV;
COPY "order" FROM '/usr/src/task-data/orders.csv' DELIMITER ',' CSV;
COPY categories FROM '/usr/src/task-data/categories.csv' DELIMITER ',' CSV;
COPY products FROM '/usr/src/task-data/products.csv' DELIMITER ',' CSV;
COPY cart_product FROM '/usr/src/task-data/cart_products.csv' DELIMITER ',' CSV;