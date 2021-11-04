-- all ended rents
create view ended_rents as
	select * from orders where (date(renting_date) + renting_period) < now() order by renting_date;

-- all cars by companies
create view cars_by_company as
	select m2."name" as company, m."name" as car_model from cars c
		join models m on c.model_id = m.model_id
		join manufacturers m2 on m.manufacturer_id = m2.manufacturer_id
		group by m2."name", m."name"
		order by m2.name, m."name";

-- all branches addresses
create materialized view branches_addresses as
	select b."name" as branch, c."name" as city, s."name" as street, b2."name" as building from branches b
		join addresses a  on a.address_id = b.address_id
		join cities c on c.city_id = a.city_id
		join streets s on s.street_id = a.street_id
		join buildings b2 on b2.building_id = a.building_id
		order by c."name";

