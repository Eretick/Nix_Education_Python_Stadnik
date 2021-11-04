-- drop database if exists cars_shop;
-- create database cars_shop;

-- creating tables
create table orders (
	order_id serial primary key,
	customer_id integer not null,
	car_id integer not null,
	price integer not null,
	branch_id integer not null,
	renting_date timestamp default now(),
	renting_period integer not null
);

create table cars(
    car_id serial primary key,
    model_id integer not null,
    color_id integer not null
);

create table colors(
    color_id serial primary key,
    color_value varchar(255) not null,
    color_name varchar(255) not null
);

create table models(
    model_id serial primary key,
    manufacturer_id integer not null,
    name varchar(255) not null
);

create table manufacturers(
    manufacturer_id serial primary key,
    name varchar not null
);

create table branches(
    branch_id serial primary key,
    name varchar(255) not null,
    address_id integer not null
);

create table customers(
    customer_id serial primary key,
    first_name varchar(255) not null,
    second_name varchar(255) not null,
    phone varchar not null,
    address_id integer not null
);

create table addresses(
    address_id serial primary key,
    city_id integer not null,
    street_id integer not null,
    building_id integer not null
);

create table streets(
    street_id serial primary key,
    name varchar(255) not null
);

create table buildings(
    building_id serial primary key,
    name varchar(255) not null
);

create table cities(
    city_id serial primary key,
    name varchar(255) not null
);

-- setup tables references
alter table addresses
	add constraint addresses_city_id_fk
	foreign key (city_id) references cities (city_id);

alter table addresses
	add constraint addresses_street_id_fk
	foreign key (street_id) references streets (street_id);

alter table addresses
	add constraint addresses_building_id_fk
	foreign key (building_id) references buildings (building_id);

alter table branches
	add constraint branches_address_id_fk
	foreign key (address_id) references addresses (address_id);

alter table customers
	add constraint customers_address_id_fk
	foreign key (address_id) references addresses (address_id);

alter table orders
	add constraint orders_branch_id_fk
	foreign key (branch_id) references branches (branch_id);

alter table orders
	add constraint orders_customer_id_fk
	foreign key (customer_id) references customers (customer_id);

alter table orders
	add constraint orders_car_id_fk
	foreign key (car_id) references cars (car_id);

alter table cars
	add constraint cars_color_id_fk
	foreign key (color_id) references colors (color_id);

alter table cars
	add constraint cars_model_id_fk
	foreign key (model_id) references models (model_id);

alter table models
	add constraint models_manufacturer_id_fk
	foreign key (manufacturer_id) references manufacturers (manufacturer_id);

--drop function if exists fill_adresses_parts_table;
--create or replace procedure fill_adresses_parts_table(in rows_num integer, in table_name varchar, in restart_fill varchar default 'no')
--language plpgsql as
--$$
--	declare
--		i record;
--		default_val varchar := '';
--		line_command varchar;
--	begin
--		if table_name = 'cities' then
--			default_val := 'city';
--			if restart_fill = 'yes' then
--				alter sequence cities_city_id_seq restart with 1;
--			end if;
--		elsif table_name = 'streets' then
--			default_val := 'street';
--			if restart_fill = 'yes' then
--				alter sequence streets_city_id_seq restart with 1;
--			end if;
--		elsif table_name = 'buildings' then
--			default_val := 'building';
--			if restart_fill = 'yes' then
--				alter sequence buildings_building_id_seq restart with 1;
--			end if;
--		end if;
--		for i in 1..rows_num
--		loop
--			raise notice '% %', i, quote_ident(table_name);
--			perform 'insert into % (name) values (%s || %);', quote_ident(table_name), default_val, i;
--		end loop;
--
--	end;
--$$;
--
--call fill_adresses_parts_table(5, 'cities', 'yes');


-- functions for filling tables with auto generated data
drop function if exists fill_cities;
create or replace procedure fill_cities(in rows_num integer, in restart_fill varchar default 'no')
language plpgsql as
$$
	declare
		i record;
	begin
		if restart_fill = 'yes' then
			delete from cities;
			alter sequence cities_city_id_seq restart with 1;
		end if;
		for i in 1..rows_num
		loop
			insert into cities (name) values ('city' || i);
		end loop;

	end;
$$;

drop function if exists fill_streets;
create or replace procedure fill_streets(in rows_num integer, in restart_fill varchar default 'no')
language plpgsql as
$$
	declare
		i record;
	begin
		if restart_fill = 'yes' then
			delete from streets;
			alter sequence streets_street_id_seq restart with 1;
		end if;
		for i in 1..rows_num
		loop
			insert into streets (name) values ('street' || i);
		end loop;

	end;
$$;

drop function if exists fill_buildings;
create or replace procedure fill_buildings(in rows_num integer, in restart_fill varchar default 'no')
language plpgsql as
$$
	declare
		i record;
	begin
		if restart_fill = 'yes' then
			delete from buildings;
			alter sequence buildings_building_id_seq restart with 1;
		end if;
		for i in 1..rows_num
		loop
			insert into buildings (name) values ('building' || i);
		end loop;

	end;
$$;

-- function for generating useful random number in range
CREATE OR REPLACE FUNCTION random_between(low INT ,high INT)
RETURNS INT language plpgsql AS
$$
BEGIN
   RETURN floor(random()* (high-low + 1) + low);
END;
$$;

drop function if exists fill_addresses;
create or replace procedure fill_addresses(in rows_num integer, in restart_fill varchar default 'no')
language plpgsql as
$$
	declare
		i record;
		city_count integer;
		street_count integer;
		building_count integer;
	begin
		if restart_fill = 'yes' then
			delete from addresses;
			alter sequence addresses_address_id_seq restart with 1;
		end if;
		select count(*) into city_count from cities;
		select count(*) into street_count from streets;
		select count(*) into building_count from buildings;
		for i in 1..rows_num
		loop
			insert into addresses (city_id, street_id, building_id)
				values (random_between(1, city_count)::integer,
						random_between(1, street_count)::integer,
						random_between(1, building_count)::integer);
		end loop;

	end;
$$;

-- function for generating random phone number
create or replace function random_phone_number()
returns varchar language plpgsql as
$$
	declare
		number varchar := '+';
	begin
		for i in 1..12
		loop
			number = concat(number, random_between(0, 9));
		end loop;
		return number;
	end;
$$;

drop function if exists fill_customers;
create or replace procedure fill_customers(in rows_num integer, in restart_fill varchar default 'no')
language plpgsql as
$$
	declare
		i record;
		addresses_count integer;
	begin
		if restart_fill = 'yes' then
			delete from customers;
			alter sequence customers_customer_id_seq restart with 1;
		end if;
		select count(*) into addresses_count from addresses;
		for i in 1..rows_num
		loop
			insert into customers (first_name, second_name, phone, address_id)
				values ('first_name' || i,
						'second_name' || i,
						random_phone_number(),
						random_between(1, addresses_count)::integer);
		end loop;

	end;
$$;

drop procedure if exists fill_branches;
create or replace procedure fill_branches(IN rows_num integer, IN restart_fill varchar default 'no')
language plpgsql
AS $$
	declare
		i record;
		addresses_count integer;
	begin
		if restart_fill = 'yes' then
			delete from branches;
			alter sequence branches_branch_id_seq restart with 1;
		end if;
		select count(*) into addresses_count from addresses;
		for i in 1..rows_num
		loop
			insert into branches ("name", address_id)
				values ('branch_name' || i,
						random_between(1, addresses_count)::integer);
		end loop;

	end;
$$;


drop function if exists fill_manufacturers;
create or replace procedure fill_manufacturers(in rows_num integer, in restart_fill varchar default 'no')
language plpgsql as
$$
	declare
		i record;
	begin
		if restart_fill = 'yes' then
			delete from manufacturers;
			alter sequence manufacturers_manufacturer_id_seq restart with 1;
		end if;
		for i in 1..rows_num
		loop
			insert into manufacturers (name)
				values ('manufacturer' || i);
		end loop;

	end;
$$;

drop function if exists fill_models;
create or replace procedure fill_models(in rows_num integer, in restart_fill varchar default 'no')
language plpgsql as
$$
	declare
		i record;
		manufacturers_count integer;
	begin
		if restart_fill = 'yes' then
			delete from models;
			alter sequence models_model_id_seq restart with 1;
		end if;
		select count(*) into manufacturers_count from manufacturers;
		for i in 1..rows_num
		loop
			insert into models (manufacturer_id, "name")
				values (random_between(1, manufacturers_count),
						'model' || i);
		end loop;

	end;
$$;

create or replace function random_color()
returns varchar language plpgsql as
$$
	declare
		color varchar := '#';
		letters varchar array := '{"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"}';
		letter_index integer;
	begin
		for i in 1..6
		loop
			letter_index = random_between(0, 15);
			color = concat(color, letters[letter_index]);
		end loop;
		return color;
	end;
$$;

drop function if exists fill_colors;
create or replace procedure fill_colors(in rows_num integer, in restart_fill varchar default 'no')
language plpgsql as
$$
	declare
		i record;
		manufacturers_count integer;
	begin
		if restart_fill = 'yes' then
			delete from colors;
			alter sequence colors_color_id_seq restart with 1;
		end if;
		select count(*) into manufacturers_count from manufacturers;
		for i in 1..rows_num
		loop
			insert into colors (color_value, color_name)
				values (random_color(),
						'color' || i);
		end loop;

	end;
$$;

drop function if exists fill_cars;
create or replace procedure fill_cars(in rows_num integer, in restart_fill varchar default 'no')
language plpgsql as
$$
	declare
		i record;
		models_count integer;
		colors_count integer;
	begin
		if restart_fill = 'yes' then
			delete from cars;
			alter sequence cars_car_id_seq restart with 1;
		end if;
		select count(*) into models_count from models;
		select count(*) into colors_count from colors;
		for i in 1..rows_num
		loop
			insert into cars (model_id, color_id)
				values (random_between(1, models_count),
						random_between(1, colors_count));
		end loop;
	end;
$$;

drop function if exists fill_orders;
create or replace procedure fill_orders(in rows_num integer, in restart_fill varchar default 'no')
language plpgsql as
$$
	declare
		i record;
		cars_count integer;
		branchs_count integer;
		customer_count integer;
	begin
		if restart_fill = 'yes' then
			delete from orders;
			alter sequence orders_order_id_seq restart with 1;
		end if;
		select count(*) into cars_count from cars;
		select count(*) into branchs_count from branches;
		select count(*) into customer_count from customers;
		for i in 1..rows_num
		loop
			insert into orders (customer_id, car_id, price, branch_id, renting_date, renting_period)
				values (random_between(1, customer_count),
						random_between(1, cars_count),
						random_between(80, 1350),
						random_between(1, branchs_count),
						date('2021-07-01') + random_between(1, 16),
						random_between(1, 15));
		end loop;
	end;
$$;


-- filling data
begin transaction;
    call fill_cities(1500);
    call fill_streets(4500);
    call fill_buildings(14500);
    call fill_addresses(1500, 'yes');
    call fill_branches(140, 'yes');
    call fill_customers(20000, 'yes');
    call fill_manufacturers(30, 'yes');
    call fill_models(120, 'yes');
    call fill_colors(50, 'yes');
    call fill_cars(880, 'yes');
    call fill_orders(18580, 'yes');
commit;