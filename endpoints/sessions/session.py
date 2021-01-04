from flask import Flask, session, request, Blueprint, jsonify, Response

bp = Blueprint("session blueprint", __name__)

global sessions
sessions = {}
@bp.route("/create_session", methods=["POST", "GET"])
def create_session(username=None, staff=False):
	try:
		sess = sessions.get(request.remote_addr)
		if "username" in sess:
			return jsonify(error={"message": "SESSION ALREADY HAS ID/USERNAME"})
	except:
		pass

	if username is None:
		username = request.json.get("username")

	session["username"] = username
	session["staff"] = staff
	sessions[request.remote_addr] = session.copy()
	return jsonify(data={"session_id" : session["username"], "staff" : session["staff"]})

#  curl -d '{"username":"waiter@waiter.com"}' -H "Content-type: application/json"  -X POST "127.0.0.1:5000/make_session"

@bp.route("/get_session_id", methods=["POST", "GET"])
def get_session_id():
	try:
		session = sessions.get(request.remote_addr)
		return jsonify(data={"session_id" : session["username"], "staff": session["staff"]})
	except:
		return jsonify(error={"message": "SESSION DOES NOT HAVE ID/USERNAME", "success" : False})

@bp.route("/get_session_is_staff", methods=["POST"])
def get_session_is_staff():
	try:
		session = sessions.get(request.remote_addr)
		return jsonify(data={"staff" : session["staff"]})
	except:
		return jsonify(error={"massage" : "NO ACTIVE SESSION", "success" : False})

@bp.route("/remove_session", methods=["POST", "GET"])
def remove_session(passed_request=None):
	if passed_request is None:
		session = sessions.get(request.remote_addr)
	else:
		session = sessions.get(passed_request.remote_add)

	if "username" in session:
		username_to_rm = session.pop("username", None)
		session.pop("staff", None)
		return jsonify(data={"removed_session_id" : username_to_rm, "success" : True})
	else:
		return jsonify(error={"success": False, "message": "SESSION WITH GIVEN ID DOES NOT EXIST"})
