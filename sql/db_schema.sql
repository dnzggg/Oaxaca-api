DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS waiter CASCADE;
DROP TABLE IF EXISTS table_details CASCADE;
DROP TABLE IF EXISTS item_type CASCADE;
DROP TABLE IF EXISTS menu CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS ordered_items CASCADE;
DROP TABLE IF EXISTS waiter_notifications CASCADE;
DROP TABLE IF EXISTS customer_notifications CASCADE;

DROP TYPE IF EXISTS order_state CASCADE;

CREATE TYPE order_state AS ENUM (
		'requested',
		'cooking',
		'ready_to_deliver',
		'delivered',
		'paid',
		'cancelled',
		'error'
	);

-- Credit for order events and function:
-- https://felixge.de/2017/07/27/implementing-state-machines-in-postgresql.html

SET timezone = 'GMT';

CREATE TABLE customer(
	email varchar(128) PRIMARY KEY,
	firstname varchar(64),
	lastname varchar(64),
	password varchar(256)
);

CREATE TABLE waiter(
	email varchar(128) PRIMARY KEY,
	firstname varchar(64),
	lastname varchar(64),
	phone_number char(11),
	password varchar(256)
);

CREATE TABLE waiter_notifications(
	notification_id serial PRIMARY KEY,
	waiter_email varchar(128) REFERENCES waiter(email),
	customer_email varchar(128) REFERENCES customer(email),
	message varchar(256)
);

CREATE TABLE table_details(
	table_number integer PRIMARY KEY,
	waiter_id varchar(128) REFERENCES waiter(email)
);

CREATE TABLE item_type(
	id integer PRIMARY KEY,
	type varchar(15)
);

CREATE TABLE menu(
	id integer PRIMARY KEY,
	name varchar(128),
	description varchar(512),
	vegan boolean,
	gluten_free boolean,
	vegetarian boolean,
	calories integer,
	price money,
	available boolean,
	food_type integer REFERENCES item_type(id),
	image varchar(2048)
);

CREATE TABLE orders(
	id serial PRIMARY KEY,
	cust_id varchar(128) REFERENCES customer(email) NOT NULL,
	table_number integer REFERENCES table_details(table_number),
	state order_state DEFAULT 'requested',
	ordered_time TIMESTAMP
);

CREATE TABLE ordered_items(
	ordered_item_id serial PRIMARY KEY,
	order_id integer REFERENCES orders(id),
	menu_item_id integer REFERENCES menu(id)
);
