from flask import Flask, request, jsonify, Blueprint
try:
	from . import validate_notifications as vn
except:
	import validate_notifications as vn
	
from common import connector


bp = Blueprint("notification blueprint", __name__)


@bp.route("/add_waiter_notification", methods=["POST"])
def add_waiter_notification():
	error = vn.validate_notification(request)
	if error:
		return(error)
	
	message = request.json.get("message")
	waiter_email = request.json.get("waiter_email")
	customer_email = request.json.get("customer_email")

	query = "INSERT INTO waiter_notifications(waiter_email, customer_email, message) VALUES(%s, %s, %s)"
	connector.execute_insert_query(query, (waiter_email, customer_email, message))

	return jsonify(data={"added_message" : message, "from" : waiter_email, "to" : customer_email, "success" : True})


@bp.route("/get_waiter_notifications", methods=["POST"])
def get_waiter_notifications():
	error = vn.validate_get_waiter_notifications(request)
	if error:
		return(error)

	waiter_email = request.json.get("waiter_email")

	query = "SELECT * FROM waiter_notifications WHERE waiter_email=%s"
	notifications = connector.execute_query(query, (waiter_email,))
	
	return jsonify(data={"notifications" : notifications, "success" : True})
	

@bp.route("/clear_waiter_notifications", methods=["POST"])
def clear_waiter_notifications():
	error = vn.validate_clear_waiter_notifications(request)
	if error:
		return(error)

	waiter = request.json.get("waiter_email")

	query = "DELETE FROM waiter_notifications WHERE waiter_email=%s"
	connector.execute_insert_query(query, (waiter,))

	return jsonify(data={"success" : True})
