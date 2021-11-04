-- get all cars by all manufacturers or by specific manufacturer.
-- Returns table
create or replace function manufactirer_cars(in manufactirer_name varchar default null)
returns table (car_id integer, car_name varchar)
language plpgsql as
$$
    result table (car_id integer, car_name varchar);
	begin
		if manufactirer_name is not null then
			return query select c.car_id, m2."name" from manufacturers m
							join models m2 on m.manufacturer_id = m2.model_id
							join cars c on c.model_id = m2.model_id
							where m.name = manufactirer_name;
		else
			return query select c.car_id, m2."name" from manufacturers m
							join models m2 on m.manufacturer_id = m2.model_id
							join cars c on c.model_id = m2.model_id;
		end if;
	end;
$$;

select manufactirer_cars('manufacturer1');
select manufactirer_cars();


-- function with loop and cursor
-- changes order's price by sale integer percent for specific car
create or replace function change_price_by_sale(in car_name varchar, in sale_percent integer)
returns void
language plpgsql as
$$
declare
	cur_prices cursor for select o.order_id, o.price, m.name as car_name, b.name as branch_name from orders o
	join branches b on o.branch_id = b.branch_id
	join cars c on c.car_id = o.car_id
	join models m on c.model_id = m.model_id;
	rec record;
begin
	open cur_prices;
	loop
		fetch cur_prices into rec;
		if rec.car_name = car_name then
			rec.price = (rec.price / 100) * sale_percent;
			update orders set price = rec.price where order_id = rec.order_id;
		end if;
		exit when not found;
		raise notice '%, %, %', rec.order_id, rec.car_name, rec.price;
	end loop;
end;
$$;


begin transaction;
select * from orders;
select change_price_by_sale('model67', 30);
select * from orders;
rollback;