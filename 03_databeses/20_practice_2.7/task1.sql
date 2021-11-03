drop function if exists zero_city_shipping_total;
create or replace function zero_city_shipping_total(x varchar)
	returns void language plpgsql as
	$$
		declare
			row record;
		begin
			for row in select * from "order" o
                join carts c on o.order_id=c.cart_id
				join users u on c.users_user_id=u.user_id
			loop
				if row.city = x then
					raise notice 'found order with city 15 with id %', row.order_id;
					update "order" set shipping_total = 0 where row.order_id="order".order_id ;
				end if;
			end loop;
		end;
	$$
;



begin transaction;
	--	looking on current values
	select shipping_total, city from "order" o
	    join carts c on o.order_id=c.cart_id
		join users u on c.users_user_id=u.user_id;
	--	make changes
	select zero_city_shipping_total('city 15');
	--	looking on result
	select shipping_total, city from "order" o
		join carts c on o.order_id=c.cart_id
		join users u on c.users_user_id=u.user_id;
rollback;