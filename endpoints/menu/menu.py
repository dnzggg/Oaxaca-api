from flask import Flask, request, jsonify, Blueprint
from common import connector, validate_functions as vf


bp = Blueprint("menu blueprint", __name__)


@bp.route("/menu", methods=["POST"])
def menu():
	# try and get the variable from the json
	try:
		getAll = request.json.get("getAll")
		if isinstance(getAll, bool):
			jsonify(error={"success": False, "message": "getAll was not a boolean"})
	except AttributeError as error:	 # if getAll not provided handle error thrown
		getAll = None

	if getAll is None or getAll is False:  # if there are no arguments select everything
		#  gets the whole menu from the database and gets the menu item type i.e. side, main ect
		#  this sql query returns the result as an already formatted json
		query = "SELECT json_agg (menu) FROM (" \
					"SELECT menu.id, name, description, vegan, " \
					"gluten_free, vegetarian, calories, price, available, type, image " \
					"FROM menu, item_type " \
					"WHERE item_type.id = menu.food_type " \
					"AND menu.available = true " \
				") AS menu;"
		result = connector.execute_query(query)
		# gets the result from the database
		return jsonify(data={"items": result[0][0]})

	elif getAll is True:
		query = "SELECT json_agg (menu) FROM (" \
					"SELECT menu.id, name, description, vegan, " \
					"gluten_free, vegetarian, calories, price, available, type, image " \
					"FROM menu, item_type " \
					"WHERE item_type.id = menu.food_type "\
					"ORDER BY menu.id"\
				") AS menu;"
		result = connector.execute_query(query)
		return jsonify(data={"items": result[0][0]})


@bp.route("/menu_item_availability", methods=["POST"])
def change_availability():
	error = vf.sent_expected_values(["newState", "menuId"], request)
	if error:
		return error

	newState = request.json.get("newState")
	menuId = request.json.get("menuId")
	query = "UPDATE menu SET available = %s WHERE id = (%s)"
	result=connector.execute_insert_query(query, (newState, menuId))
	if result is False:
		return jsonify(error={"success": False, "message": "Error MenuId does not exist"})
	return jsonify(data={"success": True})
# to Test this endpoint use
# curl -X POST -H "Content-Type: application/json" -d '{"menuId": "1","newState":"False"}' 127.0.0.1:5000/menu_item_availability
