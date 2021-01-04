from flask import request, jsonify
from common import connector
import json


# This takes a table number and ensures there is a waiter assigned to it
# otherwise it will assign the waiter with the smallest amount of tables
def auto_assign_waiter(table_num):
	# check if there are waiters in the database
	result = connector.execute_query("SELECT email FROM waiter")
	if len(result) == 0:
		error_msg = "No waiters in the database!"
		return jsonify(error = {"success":False, "message":error_msg})

    # adding a check to ensure there is a waiter assigned to the table when a order is created
	query = "SELECT waiter_id, table_number FROM table_details WHERE table_number = %s AND waiter_id IS NULL"
	result = connector.execute_query(query, (table_num,))
	if len(result) == 0 or result[0][0] is None:
		# first check if there are waiters that are not assinged to any tables
		waiters = connector.execute_query("SELECT email FROM waiter")
		assignedWaiters = connector.execute_query("SELECT waiter_id FROM table_details")
		for waiter in waiters:
			if waiter not in assignedWaiters:
				query = "UPDATE table_details SET waiter_id = %s WHERE table_number = %s"
				connector.execute_insert_query(query,(waiter[0], table_num))
				return None
		# Select the waiter with the least tables
		query = "SELECT waiter_id, COUNT(table_number) "\
				"FROM table_details "\
				"WHERE waiter_id IS NOT NULL "\
				"GROUP BY waiter_id "\
				"ORDER BY count"
		result = connector.execute_query(query)
		# we ordered by count so the top result will be the waiter with minimal tables
		waiter_email = result[0][0]

		query = "UPDATE table_details SET waiter_id = %s WHERE table_number = %s"
		connector.execute_insert_query(query,(waiter_email, table_num))


# goes through all expected values and checks if they exist in the request
# returns error message if not found or if nothing was sent in the request
def sent_expected_values(expected_values, request):
	if request.json is None:
		error_msg = "Nothing given in json, Expected "
		error_msg += ", ".join(expected_values)
		return jsonify(error={"success": False, "message": error_msg})

	for value in expected_values:
		if value not in request.json:
			error_msg = "Expected '" + value + "' argument, but was not given"
			return jsonify(error = {"success":False, "message": error_msg})
	return None
