--                                     TRANSACTION #1
begin;
	insert into order_status (order_status_id, status_name) values('6', 'Reverted');
	select * from order_status;
	savepoint inserted;
	update order_status set status_name='wrong' where status_name='Reverted';
	select * from order_status;
	rollback to savepoint inserted;
	alter table order_status add column commentary varchar(255) default '';
	select * from order_status;
-- cancel everything
rollback;
select * from order_status;

--                                     TRANSACTION #2
begin transaction;
	--	insert new status
	insert into potential_customers (id, email, name, surname, second_name, city)
	    values ('8', 'email8@mail.com', 'Jessy', 'J.', 'Scopelfild', 'New York');
	select * from potential_customers;
	savepoint inserted;
	-- delete this record
	delete from potential_customers where id='8';
	select * from potential_customers pc ;
	-- deleting everything from table
	delete from potential_customers ;
	select * from potential_customers;
	-- back to inserted new value
	rollback to savepoint  inserted;
	-- change city for inserted row
	update potential_customers set city='city3' where id = 8;
	select * from potential_customers;
-- confirm changes
commit;

--                                      TRANSACTION #3
begin transaction;
	savepoint default_state;
	--	oh no! Here is some hacker changed all costs to 0!
	update "order" set  total=0;
	--	look what he did!!!
	select * from "order";
    --	it's awesome we use transaction for everything
    --  so just screw this guy!
    rollback to savepoint default_state;
    -- see? everything is ok!
    select * from "order";
    -- lets just imagine we don't need shipping price
    update "order" set shipping_total=0;
    -- enjoy for now
    select * from "order";
-- well, finally back to real life
rollback
