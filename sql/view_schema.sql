DROP VIEW IF EXISTS ordered_items_and_price;
DROP VIEW IF EXISTS total_order_price;
DROP VIEW IF EXISTS ordered_item_and_quantity;
DROP VIEW IF EXISTS ordered_item_array;
DROP VIEW IF EXISTS all_order_details;

CREATE VIEW ordered_items_and_price AS
	SELECT ordered_item_id, order_id, menu_item_id, price
	FROM menu, ordered_items
	WHERE menu_item_id = id;

CREATE VIEW total_order_price AS
	SELECT order_id, sum(price) AS price
	FROM ordered_items_and_price
	GROUP BY order_id;

CREATE VIEW ordered_item_and_quantity AS
  SELECT order_id, name, count(name) AS quantity, count(name)*price as total
  FROM ordered_items, menu
  WHERE menu_item_id = id
  GROUP BY order_id, name, price;

CREATE VIEW ordered_item_array AS
  SELECT order_id, json_agg(
      json_build_object('name', name, 'quantity', quantity, 'cumulative_price', total)
    ) AS items
  FROM ordered_item_and_quantity
  GROUP BY order_id;

CREATE VIEW all_order_details AS
	SELECT id, table_number, state, ordered_time, price, items
	FROM orders, total_order_price, ordered_item_array
	WHERE orders.id = total_order_price.order_id
	AND orders.id = ordered_item_array.order_id;
