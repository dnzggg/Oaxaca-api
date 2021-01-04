from flask import Flask, request, jsonify, Blueprint
from common import connector
from . import validate_sign_up

bp = Blueprint("signup blueprint", __name__)

@bp.route("/signup", methods=["POST"])
def sign_up():
    error = validate_sign_up.validate_customer(request)
    if error:
        return error

    #  Get the details of the user from a post request as a json
    email = request.json.get('email')
    password = request.json.get('password')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')

    query = "INSERT INTO customer VALUES (%s, %s, %s, %s);"
    result = connector.execute_insert_query(query, (email, firstname, lastname, password))
    # if the sql INSERT doesn't work it reverts the statement to prevent data corruption
    if result is False:
        return jsonify(error = {"success": False, "message": "Query failed invalid input"})

    return jsonify(data = {"success": True})

@bp.route("/waiter_signup", methods=["POST"])
def waiter_sign_up():
    error = validate_sign_up.validate_waiter(request)
    if error:
        return error

    email = request.json.get('email')
    password = request.json.get('password')
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    phone_number = request.json.get('phone_number')

    query = "INSERT INTO waiter (email,firstname, lastname, phone_number, password) VALUES (%s,%s,%s,%s,%s)"
    result = connector.execute_insert_query(query, (email, firstname, lastname, phone_number, password))
    if not result:
        return jsonify(error = {"success": False, "message": "Query failed invalid input"})


    return jsonify(data = {"success": True})

#  Temporary test commands

#  curl -d '{"email":"testing@test.com", "password":"password", "firstname":"DELETE", "lastname":"ME"}' -H "Content-type: application/json"  -X POST "127.0.0.1:5000/sign_up"
#  this should return a json saying if it was successful or not
