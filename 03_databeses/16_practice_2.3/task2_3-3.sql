SELECT category_title, COUNT(category_title) FROM products
    JOIN categories ON products.category_id=categories.category_id
    GROUP BY category_title, products.category_id
    ORDER BY COUNT DESC;