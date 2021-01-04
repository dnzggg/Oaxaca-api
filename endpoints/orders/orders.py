from flask import Flask, request, jsonify, Blueprint
from . import validate_orders
from common import connector, validate_functions as vf


bp = Blueprint("order blueprint", __name__)


@bp.route("/create_order", methods=["POST"])
def create_order():
	error = validate_orders.validate(request)
	if error:
		return(error)

	table_num = int(request.json.get("table_num"))
	# Assign waiter to table if no one is assigned
	vf.auto_assign_waiter(table_num)

	items = request.json.get("items")
	customer = request.json.get("customer")

	query = "INSERT INTO orders (table_number, ordered_time, cust_id) VALUES (%s, NOW(), %s) RETURNING id"
	result = connector.execute_query(query, (int(table_num), customer))
	order_id = result[0]

	items_added = []
	# because we are given a list of menu items we have to loop through and add them one by one
	for menu_item_id in items:
		try:
			query = "INSERT INTO ordered_items (order_id, menu_item_id) VALUES (%s, %s)"
			connector.execute_insert_query(query, (order_id, menu_item_id))
			items_added.append(menu_item_id)
		except:
			error_msg = "Problem adding items to ordered_items, likely an invalid menu_item_id"
			return jsonify({"success" : False, "message" : error_msg})

	return jsonify(data={"success" : True, "order_id" : order_id, "items_added" : items_added})


@bp.route("/order_event", methods=["POST"])
def order_event():
	error =	validate_orders.validate_order_event(request)
	if error:
		return(error)

	order_id = request.json.get("order_id")
	event = request.json.get("order_event")

	query = "INSERT INTO order_events(order_id, event) VALUES(%s, %s)"
	connector.execute_insert_query(query, (order_id, event))

	return jsonify(data={"success" : True})


@bp.route("/get_order", methods=["POST"])
def get_order():
	error = validate_orders.validate_get_order(request)
	if error:
		return (error)

	order_id = request.json.get("order_id")
	cust_id = request.json.get("cust_id")

	# Selects all relevant information about the order including the quantity of each item and the total price
	# where the order id and customer id are equal to values given above
	query = "SELECT json_agg (order_list) FROM " \
				"(SELECT id, table_number, state, to_char(ordered_time, 'HH:MI') as ordered_time, price, items " \
				"FROM orders, total_order_price, ordered_item_array " \
				"WHERE orders.id = total_order_price.order_id " \
				"AND orders.id = ordered_item_array.order_id " \
				"AND orders.cust_id = %s "\
				"AND orders.id = %s) " \
			"AS order_list;"
	result = connector.execute_query(query, (cust_id, order_id))
	return jsonify(data = {"order": result[0][0]})


@bp.route("/get_orders", methods=["POST"])
def get_orders():
	error = validate_orders.validate_get_orders(request)
	if error:
		return (error)

	states = request.json.get("states")

	# handles case for getting all orders:
	if len(states) == 0:
		# Selects all relevant information about the order including the quantity of each item and the total price
		query = "SELECT json_agg (order_list) FROM " \
					"(SELECT id, table_number, state, to_char(ordered_time, 'HH:MI') as ordered_time, price, items " \
					"FROM orders, total_order_price, ordered_item_array " \
					"WHERE orders.id = total_order_price.order_id " \
					"AND orders.id = ordered_item_array.order_id " \
					"AND DATE(ordered_time) = DATE(NOW()) " \
					"ORDER BY ordered_time )" \
				"AS order_list;"
		result = connector.execute_query(query)
	else:
		query = "SELECT json_agg (order_list) FROM " \
					"(SELECT id, table_number, state, to_char(ordered_time, 'HH:MI') as ordered_time, price, items " \
					"FROM orders, total_order_price, ordered_item_array " \
					"WHERE orders.id = total_order_price.order_id " \
					"AND orders.id = ordered_item_array.order_id " \
					"AND DATE(ordered_time) = DATE(NOW()) " \
				"AND state = ANY('{"
		# adds all order states so it selects orders that are in any of those states
		query += ", ".join(states) + "}') "
		query += "ORDER BY ordered_time) AS order_list;"
		result = connector.execute_query(query)
	return jsonify(data={"orders" : result[0][0]})


@bp.route("/get_waiters_orders", methods=["POST"])
def get_waiter_orders():
	error = validate_orders.validate_get_waiters_orders(request)
	if error:
		return error

	states = request.json.get("states")
	waiter_id = request.json.get("waiter_id")

	# handles case for getting all orders:
	if len(states) == 0:
		# Selects all relevant information about the order including the quantity of each item and the total price
		# where the waiter id are equal to value given above
		query = "SELECT json_agg (order_list) FROM " \
					"(SELECT id, all_order_details.table_number, state, to_char(ordered_time, 'HH:MI') AS ordered_time, price, items " \
					"FROM all_order_details, table_details " \
					"WHERE all_order_details.table_number = table_details.table_number "\
					"AND waiter_id = %s " \
					"AND DATE(ordered_time) = DATE(NOW()) " \
				"ORDER BY ordered_time) "\
				"AS order_list;"

		result = connector.execute_query(query, (waiter_id,))
	else:
		query = "SELECT json_agg (order_list) FROM " \
					"(SELECT id, all_order_details.table_number, state, to_char(ordered_time, 'HH:MI') AS ordered_time, price, items " \
					"FROM all_order_details, table_details " \
					"WHERE all_order_details.table_number = table_details.table_number "\
					"AND waiter_id = %s " \
					"AND DATE(ordered_time) = DATE(NOW()) " \
				"AND state = ANY('{"
		query += ", ".join(states) + "}') "
		query += "ORDER BY ordered_time ) "
		query += "AS order_list;"
		result = connector.execute_query(query, (waiter_id,))
	return jsonify(data={"orders" : result[0][0]})


@bp.route("/get_cust_orders", methods=["POST"])
def get_cust_orders():
	error = validate_orders.validate_get_cust_order(request)
	if error:
		return (error)

	id = request.json.get("cust_id")

	# Selects all orders for a specific customer that happened today
	query = "SELECT json_agg (order_list) FROM " \
				"(SELECT id, table_number, state, to_char(ordered_time, 'HH:MI') AS ordered_time, price, items " \
				"FROM orders, total_order_price, ordered_item_array " \
				"WHERE orders.id = total_order_price.order_id " \
				"AND orders.id = ordered_item_array.order_id " \
				"AND orders.cust_id = %s " \
				"AND DATE(ordered_time) = DATE(NOW())"\
				"ORDER BY ordered_time) " \
			"AS order_list;"
	result = connector.execute_query(query, (id,))
	return jsonify(data={"orders":result[0][0]})


@bp.route("/get_old_cust_orders", methods=["POST"])
def get_old_cust_orders():
	error = validate_orders.validate_get_cust_order(request)
	if error:
		return (error)

	id = request.json.get("cust_id")

	# Select all orders for a customer from the past
	query = "SELECT json_agg (order_list) FROM " \
				"(SELECT id, table_number, state, to_char(ordered_time, 'HH:MI') AS ordered_time, price, items " \
				"FROM orders, total_order_price, ordered_item_array " \
				"WHERE orders.id = total_order_price.order_id " \
				"AND orders.id = ordered_item_array.order_id " \
				"AND orders.cust_id = %s " \
				"AND DATE(ordered_time) < DATE(NOW())"\
				"ORDER BY ordered_time) " \
			"AS order_list;"
	result = connector.execute_query(query, (id,))
	return jsonify(data={"orders":result[0][0]})
