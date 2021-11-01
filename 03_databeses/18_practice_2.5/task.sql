-- sql from task 2.3 point 2.
-- using transaction cause analyze can affects data (and no need to remove indexes manually
begin transaction;
    -- used seq scan on "order"
    -- cost (cost=39.32..39.33 rows=1 width=32) (actual time=0.464..0.466)
    explain (analyze) SELECT MAX(total) from "order"
        WHERE order_status_order_status_id=4
        AND created_at
        BETWEEN '2020.09.10' AND '2020.12.31';
    -- creting indexes
    create index on "order"(total);
    create index on "order"(order_status_order_status_id);
    -- look again
    -- (cost=4.32..4.33 rows=1 width=32) (actual time=0.051..0.052
    explain (analyze) SELECT MAX(total) from "order"
        WHERE order_status_order_status_id=4
        AND created_at
        BETWEEN '2020.09.10' AND '2020.12.31';
-- delete indexes
rollback;


-- Seq Scan (cost=0.00..40.00 rows=1 width=28)
-- (actual time=0.471..0.472)
explain (analyze) select * from carts where total > 2000;
create index  on carts(total);
-- Index Scan
-- (cost=0.28..8.29 rows=1 width=28)
-- (actual time=0.010..0.011
explain (analyze) select * from carts where total > 2000;
drop index carts_total_idx;


begin;
	-- Aggregate  (cost=39.32..39.33 rows=1 width=32)
	-- (actual time=0.460..0.461)
	explain (analyze) SELECT MAX(total) from "order"
		WHERE order_status_order_status_id=4
		AND created_at BETWEEN '2020.09.10' AND '2020.12.31';
	create index on "order"(order_status_order_status_id);
	-- Aggregate  (cost=26.28..26.29 rows=1 width=32)
	-- (actual time=0.251..0.252)
	explain (analyze) SELECT MAX(total) from "order"
		WHERE order_status_order_status_id=4
		AND created_at BETWEEN '2020.09.10' AND '2020.12.31';
	create index on "order"(created_at);
	-- Aggregate  (cost=20.71..20.72 rows=1 width=32)
	-- (actual time=0.124..0.126)
	explain (analyze) SELECT MAX(total) from "order"
		WHERE order_status_order_status_id=4
		AND created_at BETWEEN '2020.09.10' AND '2020.12.31';
rollback;