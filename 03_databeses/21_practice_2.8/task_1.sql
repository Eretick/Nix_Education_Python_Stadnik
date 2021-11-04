drop function if exists compare_to_avg;
create or replace function compare_to_avg(product_name varchar)
returns float
language plpgsql  as
$$
	declare
		product record;
		result_ float;
		i record;
	BEGIN
		FOR i IN select p.product_title, p.price, c.category_id, c.category_title,
					avg(price) over (partition by c.category_id)
				from products p
				join categories c
				on p.category_id=c.category_id
		loop
			IF i.product_title=product_name then
			result_ := i.price /i.avg * 100;
				result_ := round(cast(result_ as numeric), 2);
				raise notice 'Product''s ''%''  price is % %% of category %''s average price.',
					i.product_title, result_, i.category_title;
				return result_;
			END IF;
		END loop;
	end;
$$


select compare_to_avg('Product 1');
