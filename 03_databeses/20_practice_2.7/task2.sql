create or replace procedure create_staff_orders_view(in func_mode varchar)
	language plpgsql as $$
		begin
--			raise notice '%', func_mode;
			if func_mode='create' then
				create or replace view staffordersview as
				select order_id, first_name||' '|| middle_name ||' '||last_name as name,
					user_id, o.total, created_at, updated_at
					from users u
					join carts c on c.users_user_id=u.user_id
					join "order" o on o.carts_cart_id=c.cart_id
					where if_staff='1';
				raise notice 'The view staffordersview could be created.';
			elsif func_mode='drop' then
				drop view  if exists staffordersview;
				raise notice 'The view staffordersview could be dropped.';
			else
				raise 'Incorrect func_mode attribute, should be ''create'' or ''drop''';
			end if;
		end;
	$$
;

create or replace procedure top_stuff_orders(in limit_number integer)
	language plpgsql as $$
	declare
		row record;
	begin
		call create_staff_orders_view('create');
		for row in select name, total from staffordersview order by total limit limit_number
		loop
			raise notice '% has spent % $. Earned % $ award.', row.name, row.total, row.total*0.03;
		end loop;
		call create_staff_orders_view('drop');
	end;
	$$
;


-- tests for procedure 1
call create_staff_orders_view('create');
select * from staffordersview;
call create_staff_orders_view('drop');
call create_staff_orders_view('some bullshit'); -- raise an error


-- tests for procedure 2
call top_stuff_orders(3)