-- creation
create view StockProductsView as select * 
	from products 
	where in_stock > 0 
	order by product_id
	with check option ; 

-- with check not working with views from 1 table
create view UnfinishedOrdersView as select carts_cart_id, shipping_total, total, created_at, updated_at 
	from "order" o 
	join order_status os ON o.order_status_order_status_id=os.order_status_id 
	where os.order_status_id=2;

-- with check is not working with select distinct
create view ProductsByCategoriesView as 
	select distinct categories.category_id, product_id, product_title, in_stock, price
		from products, categories group by categories.category_id, product_id order by category_id;

-- materialized view
create materialized view mostexpensivesells as select product_id, product_title, price, total, 
	first_name|| ' ' ||last_name as name
	from products p 
	join carts c on p.product_id=c.cart_id 
	join users u on c.users_user_id=u.user_id
	order by price desc;


-- deleting
drop view if exists productsbycategoriesview;
drop view if exists stockproductsview;
drop view if exists unfinishedordersview;
drop materialized view mostexpensivesells;
