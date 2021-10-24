SELECT * FROM products
    WHERE price>80 AND price<=150;
SELECT * FROM "order"
    WHERE created_at>='2020.01.01' ORDER BY created_at;
SELECT * FROM "order"
    WHERE created_at BETWEEN '2020.01.01' AND '2020.06.01';
SELECT * FROM products
    WHERE category_id=7
    OR category_id=11 or category_id=18;
SELECT * FROM "order" WHERE order_status_order_status_id=1
    OR order_status_order_status_id=2
    OR order_status_order_status_id=3
    AND created_at BETWEEN '2020.01.01' AND '2020.12.31';
SELECT * FROM carts
    INNER JOIN "order" ON cart_id=carts_cart_id
    WHERE order_status_order_status_id=1 OR order_status_order_status_id=5;

