SELECT * FROM products
    LEFT JOIN cart_product ON products_product_id=product_id
    WHERE carts_cart_id IS NULL;
SELECT product_title FROM products
    LEFT JOIN cart_product ON products_product_id=product_id
    LEFT JOIN carts ON carts.cart_id=cart_product.carts_cart_id
    LEFT JOIN "order" ON carts.cart_id="order".carts_cart_id
    WHERE "order".order_id IS NULL;
SELECT product_title, COUNT(product_title) FROM products
    JOIN cart_product ON cart_product.products_product_id=products.product_id
    JOIN carts ON carts_cart_id=carts.cart_id
    GROUP BY product_title
    ORDER BY COUNT
    DESC LIMIT 10;
SELECT product_title, COUNT(product_title) FROM products
    LEFT JOIN cart_product ON cart_product.products_product_id=products.product_id
    LEFT JOIN carts ON carts_cart_id=carts.cart_id
    LEFT JOIN "order" ON carts.cart_id="order".carts_cart_id
    WHERE "order".order_id IS NOT NULL
    GROUP BY product_title
    ORDER BY COUNT DESC
    LIMIT 10;
SELECT first_name, middle_name, last_name, total FROM users
    JOIN carts ON user_id=cart_id
    ORDER BY total DESC
    LIMIT 5;
SELECT order_id, first_name, middle_name, last_name, COUNT(email) FROM "order"
	LEFT JOIN carts ON carts_cart_id=cart_id
	LEFT JOIN users ON 	users_user_id=user_id
	GROUP BY order_id, cart_id, user_id, users_user_id
	ORDER by COUNT
	DESC LIMIT 5;
SELECT * FROM products
    LEFT JOIN cart_product ON products_product_id=product_id
    WHERE products_product_id IS NULL;