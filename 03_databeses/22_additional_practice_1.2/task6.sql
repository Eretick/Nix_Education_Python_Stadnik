-- trigger #1. Validate values from cities, streets and buildings tables
create or replace function log_colors_update()
returns trigger
language plpgsql as
$$
declare
	cv varchar := old.color_value;
	cn varchar := old.color_name;
begin
	if new.color_value is not null then
		cv = new.color_value;
	end if;
	if new.color_name is not null then
		cn = new.color_name;
	end if;
	if new <> old and cv not in (select c.color_value from colors c)
		and cn not in (select c.color_name from colors c) then
		return new;
	else raise 'Duplicate color insert!';
	end if;
	return new;
end;
$$;


create or replace trigger update_colors_validation_trigger
	before insert or update
	on colors
	for each row
	execute procedure log_colors_update();

--test. both must raise an errror if values already in colors table
begin transaction;
    select * from colors;
    insert into colors (color_value, color_name) values ('#7C9D', 'color50');
    update colors set color_value = '#7C9D' where color_id = 1;
rollback;

-- #2. Delete from orders log trigger
create or replace function log_orders_delete()
returns trigger
language plpgsql as
$$
begin
	create table if not exists deleted_orders(
		order_id integer,
		customer_id integer,
		car_id integer,
		price integer ,
		branch_id integer,
		renting_date timestamp,
		renting_period integer);
	raise notice '%, %', new.order_id, old.order_id;
	insert into deleted_orders(order_id, customer_id, car_id, price,branch_id, renting_date, renting_period)
		values(old.order_id, old.customer_id, old.car_id, old.price, old.branch_id, old.renting_date, old.renting_period);
	return old;
end;
$$;


create or replace trigger delete_orders_logger
	after delete
	on orders
	for each row
	execute procedure log_orders_delete();


begin transaction;
    select * from orders;
    delete from orders where order_id = 4;
    select * from orders;
    select * from deleted_orders;
rollback;