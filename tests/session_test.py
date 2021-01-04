import requests, json, sys
try:
	from . import tester
except:
	import tester

session = requests.Session()

verbose = False

test_data = {
			"username" : "example@example.com",
			"password" : "password"
			}

api_url = "http://localhost:5000/"

def test_server():
	req = session.get(api_url)
	return req, req.status_code

def test_create_session():
	req = session.post(api_url + "create_session", json={"username" : test_data["username"]})
	if verbose:
		print(req.text)
	return req, req.status_code

def test_get_session_id():
	req = session.post(api_url + "get_session_id")
	if verbose:
		print(req.text)
	return req, req.status_code

def test_get_session_is_staff():
	req = session.post(api_url + "get_session_is_staff")
	if verbose:
		print(req.text)
	return req, req.status_code

def test_remove_session():
	req = session.post(api_url + "remove_session", json={"username" : test_data["username"]})
	if verbose:
		print(req.text)
	return req, req.status_code


# the test are ran in a specific way
# the true/false values correspond to whether it should pass or fail
# true meaning it should pass, and false it should fail
tests = [
		[test_server, None],
		[test_create_session, True],
		[test_create_session, False],
		[test_get_session_id, True],
		[test_get_session_is_staff, True],
		[test_remove_session, True],
		[test_get_session_id, False],
		[test_remove_session, False],
		]

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] == "v":
			verbose = True
	total = 0
	passed = 0
	failed = []
	total, passed, failed = tester.run_tests(tests, total, passed, failed)
	tester.print_results(total, passed, failed)






