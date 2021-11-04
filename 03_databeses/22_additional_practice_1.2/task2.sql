-- request #1. Left join. Request only
-- all cars in specific branches
explain
select m.name, b."name" from cars c
	left join orders o on o.car_id = c.car_id
	left join branches b on b.branch_id = o.branch_id
	left join models m on c.model_id = m.model_id
	where b."name" = 'branch_name66';

-- request #2. Right join. Request with optimisation
-- finding specific user in users list who still did not maked orders
begin transaction;
    -- (cost=0.00..980.95)
	explain select * from orders o
			right join customers c on o.customer_id=c.customer_id
			where o.customer_id is null and c.first_name = 'first_name4';
	create index customer_name1 on customers(first_name);
	(cost=0.29..532.26)
	explain select * from orders o
			right join customers c on o.customer_id=c.customer_id
			where o.customer_id is null and c.first_name = 'first_name4';
rollback;


-- request #3. Inner join.Request and optimisation only
begin transaction;
	explain
	-- (cost=56.29..59.73)
	select b."name", c."name", s."name", b2."name" from branches b
		join addresses a  on a.address_id = b.address_id
		join cities c on c.city_id = a.city_id
		join streets s on s.street_id = a.street_id
		join buildings b2 on b2.building_id = a.building_id
		where c."name" = 'city100'
		order by c."name";
	create index city_name_idx on cities("name");
	-- (cost=36.84..40.27)
	explain
	select b."name", c."name", s."name", b2."name" from branches b
		join addresses a  on a.address_id = b.address_id
		join cities c on c.city_id = a.city_id
		join streets s on s.street_id = a.street_id
		join buildings b2 on b2.building_id = a.building_id
		where c."name" = 'city100'
		order by c."name";

rollback;