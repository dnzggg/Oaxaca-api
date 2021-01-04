from flask import Flask, request, jsonify, Blueprint, session
from endpoints import sessions
from common import connector, validate_functions as vf


bp = Blueprint("login blueprint", __name__)


# logs the user in or returns error message if incorrect details
@bp.route("/login", methods=["POST"])
def login():
	error = vf.sent_expected_values(["email", "password", "staff_login"], request)
	if error:
		return error

	email = request.json.get('email')
	password = request.json.get('password')
	staff_login = request.json.get('staff_login')

	# select the user with the email inputted
	if staff_login:
		query = "SELECT email, password FROM waiter WHERE email = %s AND password = %s"
	else:
		query = "SELECT email, password FROM customer WHERE email = %s AND password = %s"

	result = connector.execute_query(query, (email, password))

	# if the result returns nothing return invalid response
	if not result:
		return jsonify(error={"valid_credentials" : False, "message" : "invalid email or password"})
	else:
		email = result[0][0]
		sessions.session.create_session(email, staff_login)
		return jsonify(data={"valid_credentials" : True, "username" : email, "is_staff" : staff_login})


# Logs the user out using sessions
@bp.route("/logout", methods=["POST"])
def logout():
	return sessions.session.remove_session()
