SELECT state, event, order_event_transition(state, event)
FROM (VALUES
('start', 'request'),
('requested', 'confirm'),
('confirmed', 'cook'),
('cooking', 'deliver'),
('delivered', 'pay'),
('cooking', 'cancel'),
('confirmed', 'cancel')
) AS examples(state, event);

UPDATE orders SET state='start' WHERE orders.id=1;

SELECT state FROM orders;
INSERT INTO order_events(order_id, event) VALUES(1, 'request');
SELECT state FROM orders;
INSERT INTO order_events(order_id, event) VALUES(1, 'confirm');
SELECT state FROM orders;
INSERT INTO order_events(order_id, event) VALUES(1, 'start_cook');
SELECT state FROM orders;
INSERT INTO order_events(order_id, event) VALUES(1, 'cooked');
SELECT state FROM orders;
INSERT INTO order_events(order_id, event) VALUES(1, 'deliver');
SELECT state FROM orders;
INSERT INTO order_events(order_id, event) VALUES(1, 'pay');
SELECT state FROM orders;
