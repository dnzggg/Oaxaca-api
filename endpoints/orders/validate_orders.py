from flask import Flask, request, jsonify, Blueprint
from common import connector, validate_functions as vf


# Fetch list of valid states/events from DB.
enum_list = connector.execute_query('''
	SELECT type.typname,
	enum.enumlabel AS value
	FROM pg_enum AS enum
	JOIN pg_type AS type
	ON (type.oid = enum.enumtypid)
	GROUP BY enum.enumlabel,
	type.typname;
	''')

valid_events = []
valid_states = []

for enum_val in enum_list:
	name = enum_val[0]
	value = enum_val[1]
	if name == "order_state":
		valid_states.append(value)
	elif name == "order_event":
		valid_events.append(value)


def validate(request):
	error = vf.sent_expected_values(["customer", "items", "table_num"], request)
	if error:
		return error

	table_num = int(request.json.get("table_num"))
	items = request.json.get("items")
	customer = request.json.get("customer")

	if not isinstance(items, (list)):
		error_msg = "expected 'items' to be list"
		return jsonify(error={"success" : False, "message" : error_msg})

	if len(items) > 100:
		error_msg = "'items' is more than 100 items, please shorten it"
		return jsonify(error={"success" : False, "message" : error_msg})

	query = "SELECT * FROM table_details WHERE table_number = %s"
	result = connector.execute_query(query, (table_num,))
	if not result:
		error_msg =  "Given table number is not in table_detail"
		return jsonify(error={"success" : False, "message" : error_msg})

	query = "SELECT id FROM menu"
	result = connector.execute_query(query)
	res = []
	for r in result:
		res.append(int(r[0]))
	for id in items:
		if id not in res:
			error_msg = "Invalid menu_item_id given in 'items' list"
			return jsonify(error={"success" : False, "message" : error_msg})

	return None


def validate_order_event(request):
	error = vf.sent_expected_values(["order_id", "order_event"], request)
	if error:
		return error

	order_id = request.json.get("order_id")
	event = request.json.get("order_event")

	if event not in valid_events:
		error_msg = "given event is not a valid event type, see this objects 'valid_events'"
		error_msg += " for a list of valid events"
		return jsonify(error={"success" : False, "message" : error_msg, "valid_events" : valid_events})

	result = connector.execute_query("SELECT * FROM orders WHERE id=%s", (order_id,))
	if not result:
		error_msg = "Invalid order_id, given order_id is not in orders table"
		return jsonify(error={"success" : False, "message" : error_msg})

	query = "SELECT state FROM orders WHERE id = %s"
	result = connector.execute_query(query, (order_id,))
	order_state = result[0]

	query = "SELECT order_event_transition(%s, %s) AS new_state"
	result = connector.execute_query(query, (order_state, event))

	print("PRINTING FROM VALIDATE_ORDERS: ", result[0][0])
	# database will return error if there is a movement from one state to another that is not valid
	# or if the event sent is not valid, see func_schema.sql to see the inner workings
	if result[0][0] == "error":
		print("ERROR FOUND")
		error_msg = "Given event cannot be performed on this order."
		return jsonify(error={"success" : False, "message" : error_msg})

	return None


def validate_get_orders(request):
	error = vf.sent_expected_values(["states"], request)
	if error:
		return error

	states =  request.json.get("states")

	for state in states:
		if state not in valid_states:
			error_msg = "given event is not a valid event type, see this objects 'valid_states'"
			error_msg += " for a list of valid events"
			return jsonify(error={"success" : False, "message" : error_msg, "valid_states" : valid_states})

	return None


def validate_get_cust_order(request):
	error = vf.sent_expected_values(["cust_id"], request)
	if error:
		return error

	cust_id = request.json.get("cust_id")

	query = "SELECT email FROM customer where email = %s"
	result = connector.execute_query(query, (cust_id,))
	if result is None or result == []:
		error_msg = "No customer with id = " + cust_id
		return jsonify({"success":False, "message": error_msg})
	return None


def validate_get_order(request):
	# using validate functions to do common checking, if the user exists
	error = validate_get_cust_order(request)
	if error is not None:
		return error

	error = vf.sent_expected_values(["order_id"], request)
	if error:
		return error

	order_id = request.json.get("order_id")

	query = "SELECT id from orders where id = %s"
	result = connector.execute_query(query, (order_id,))
	if result is None or result == []:
		error_msg = "No order exists with id = " + order_id
		return jsonify(error={"success": False, "message": error_msg})

	return None


def validate_get_waiters_orders(request):
	# using validate functions to do common checking, here we are checking if the user exists
	error = validate_get_orders(request)
	if error is not None:
		return error

	error = vf.sent_expected_values(["waiter_id"], request)
	if error:
		return error

	waiter_id = request.json.get("waiter_id")

	query = "SELECT email from waiter where email = %s"
	result = connector.execute_query(query, (waiter_id,))
	if len(result) is 0:
		error_msg = "Given waiter email was not found in the table"
		return jsonify(error={"success":False, "message":error_msg})

	return None
