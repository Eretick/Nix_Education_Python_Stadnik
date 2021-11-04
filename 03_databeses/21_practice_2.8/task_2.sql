-- first trigger
create or replace function check_category_uniq()
	returns trigger
	language plpgsql
	as $$
	declare temp_ record;
	begin
		select category_title into temp_ from categories c 
			where c.category_title=new.category_title;    
		if found then
			raise 'Category title % is already in table!', new.category_title;
		end if;
		return new;
	end;
	$$
;

-- test for the first trigger
begin transaction;
	drop trigger if exists before_insert_category on categories;
	create trigger before_insert_category
		before insert 
		on categories 
--		for statement
		for each row 
		execute procedure check_category_uniq();
	select * from categories c ;
	-- correct insert
	insert into categories values('30', 'new category', 'new title');
	select * from categories c ;
	-- raise an error cause of not unique category name
	insert into categories values('31', 'Category 20', 'new title');
rollback;

-- second trigger
create or replace function check_order_cost()
	returns trigger
	language plpgsql
	as $$
	declare totals record;
	begin
		for totals in select total from "order"
		loop
			if new.total = 0 then
				raise 'Order''s total can''t be 0!';
			return new;
			end if;
		end loop;
		return new;
	end;
	$$
;

-- test for second trigger
begin transaction;
	drop trigger if exists befote_insert_order on "order";
	create trigger befote_insert_order
		before insert
		on "order"
		for each row
		execute procedure check_order_cost();
	select * from "order" ;
	-- correct insert
	insert into "order" values('1501', '1501', '4', '20', '435');
	select * from "order" ;
	-- raise an error cause cost is 0
	insert into "order" values('1502', '1502', '2', '56', '0');
rollback;