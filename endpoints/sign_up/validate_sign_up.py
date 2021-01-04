from flask import Flask, request, jsonify, Blueprint
from common import connector, validate_functions as vf


# checks if all the essential information is provided in request
def validate_user(request):
    error = vf.sent_expected_values(["email", "firstname", "lastname", "password"], request)
    if error:
        return error
    return None


def validate_customer(request):
    error = validate_user(request)
    if error:
        return error

    email = request.json.get('email')

    query = "SELECT email FROM customer WHERE email = %s;"
    result = connector.execute_query(query, (email,))
    # if there is someone in the database with that email already
    if len(result) == 1:
        error_msg = "Email given is already in use"
        return jsonify(error = {"success":False, "message": error_msg})

    return None


def validate_waiter(request):
    error = validate_user(request)
    if error:
        return error

    error = vf.sent_expected_values(["phone_number"], request)
    if error:
        return error

    phone_number = request.json.get('phone_number')
    # if the phone number is not an integer and of length 11
    if len(phone_number) != 11 and isinstance(phone_number, int):
        error_msg = "Phone number was not a valid input must be 07 followed by 9 digits"
        return jsonify(error = {"success":False, "message": error_msg})

    email = request.json.get('email')

    query = "SELECT email FROM waiter WHERE email = %s;"
    result = connector.execute_query(query, (email,))
    # if there is someone in the database with that email already
    if len(result) == 1:
        error_msg = "Email given is already in use"
        return jsonify(error = {"success":False, "message": error_msg})

    return None
