DROP TYPE IF EXISTS order_event CASCADE;

CREATE TYPE order_event AS ENUM (
		'start_cook',
		'cooked',
		'deliver',
		'pay',
		'cancel'
	);

--EVENT TABLE

DROP TABLE IF EXISTS order_events CASCADE;

CREATE TABLE order_events(
	id serial PRIMARY KEY,
	order_id INTEGER REFERENCES orders(id) NOT NULL,
	event order_event NOT NULL
);

--FSM FUNCTION

DROP FUNCTION IF EXISTS order_event_transition;

CREATE FUNCTION order_event_transition(state order_state, event order_event) RETURNS text
LANGUAGE sql AS
$$
	SELECT CASE state
		WHEN 'requested' THEN
			CASE event
				WHEN 'start_cook' THEN 'cooking'
				WHEN 'cancel' THEN 'cancelled'
				ELSE 'error'
			END

		WHEN 'cooking' THEN
			CASE event
				WHEN 'cancel' THEN 'cancelled'
				WHEN 'cooked' THEN 'ready_to_deliver'
				ELSE 'error'
			END
   		WHEN 'ready_to_deliver' THEN
      		CASE event
       			WHEN 'deliver' THEN 'delivered'
        		ELSE 'error'
      		END
		WHEN 'delivered' THEN
			CASE event
				WHEN 'pay' THEN 'paid'
				ELSE 'error'
			END
	END
$$;

--FUNCTION TO CALL FROM TRIGGER

DROP FUNCTION IF EXISTS new_event;

CREATE FUNCTION new_event() RETURNS trigger AS
$$
DECLARE
	old_state order_state;
	new_event order_event;
	new_state order_state;
BEGIN
	SELECT NEW.event INTO new_event;
	SELECT state FROM orders WHERE orders.id = NEW.order_id INTO old_state;
	SELECT order_event_transition(old_state, new_event) INTO new_state;

	UPDATE orders SET state=new_state WHERE orders.id = NEW.order_id;
	RETURN NEW;
END
$$
LANGUAGE PLPGSQL;

--TRIGGER

CREATE TRIGGER event_trigger
AFTER INSERT
ON order_events
FOR EACH ROW
EXECUTE PROCEDURE new_event();
