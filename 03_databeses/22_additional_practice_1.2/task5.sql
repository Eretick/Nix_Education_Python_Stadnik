-- #1  insert order procedure
create or replace procedure create_order(customer_firstname varchar, customer_secondname varchar,  car_id integer, price integer, branch_id integer, renting_period integer)
language plpgsql as
$$
	declare
		c_id integer;
	begin
		select c.customer_id into c_id from customers c
			where c.first_name = customer_firstname and c.second_name = customer_secondname;
		if found then
			raise notice 'ok, %', c_id;
			insert into orders (customer_id, car_id, price, branch_id, renting_period)
				values(c_id, car_id, price, branch_id, renting_period);
		else
			raise 'Customer not found!';
		end if;
	end

$$;

begin transaction;
	call create_order('first_name1', 'second_name1', 6, 120, 1, 8);
	select * from orders o ;
rollback;


-- #2 update/delete order procedure
create or replace procedure edit_order(
										_order_id integer,
										_customer_id integer default null,
										_car_id integer default null,
										_price integer default null,
										_branch_id integer default null,
										_renting_period integer default null,
										need_delete bool default false)
language plpgsql as
$$
	declare
		order_row record;
		e_order_id integer := _order_id;
		e_customer_id integer := _customer_id;
		e_car_id integer := _car_id;
		e_price integer := _price;
		e_branch_id integer := _branch_id;
		e_renting_period integer := _renting_period;
	begin
		select * into order_row from orders o where o.order_id = order_id;

		if e_customer_id is null then
			e_customer_id = order_row.customer_id;
		end if;
		if e_car_id is null then
			e_car_id = order_row.car_id;
		end if;
		if e_price is null then
			e_price = order_row.price;
		end if;
		if e_branch_id is null then
			e_branch_id = order_row.branch_id;
		end if;
		if e_renting_period is null then
			e_renting_period = order_row.renting_period;
		end if;

		if need_delete is false then
			update orders set customer_id=e_customer_id, car_id=e_car_id, price=e_price, branch_id=e_branch_id, renting_period=e_renting_period
				where order_id = e_order_id;
		else
			delete from orders o where o.order_id = e_order_id;
		end if;
	end;
$$;



begin transaction;
	savepoint start;
	-- look at order
	select * from orders where order_id = 1;
	-- editing different columns
	call edit_order(1, 2);
	select * from orders where order_id = 1;
	call edit_order(1, 2, 3,11111, 2, 1111112);
	select * from orders where order_id = 1;
	-- editing only last column
	rollback to savepoint start;
	select * from orders where order_id = 1;
	call edit_order(1, null, null, null, null, 1111112);
	select * from orders where order_id = 1;
	-- deleting order with passed id
	call edit_order(1, null, null, null, null, null, true);
	select * from orders where order_id = 1;
rollback;