SELECT AVG(total) from "order" WHERE order_status_order_status_id=4;
SELECT MAX(total) from "order" WHERE order_status_order_status_id=4 AND created_at BETWEEN '2020.09.10' AND '2020.12.31';
