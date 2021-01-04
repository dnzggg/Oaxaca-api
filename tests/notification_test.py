import requests, json, sys
try:
	from . import tester
except:
	import tester

session = requests.Session()

verbose = False

api_url = "http://localhost:5000/"

def test_add_waiter_notification():
	notification_json = {"waiter_email" : "waiter@waiter.com", 
						"customer_email" : "example@example.com", 
						"message" : "notification message"}

	req = session.post(api_url + "add_waiter_notification", json=notification_json)
	if verbose:
		print(req.text)
	return req, req.status_code


def test_get_waiter_notifications():
	req = session.post(api_url + "get_waiter_notifications", json={"waiter_email" : "waiter@waiter.com"})
	if verbose:
		print(req.text)
	return req, req.status_code
	

def test_clear_waiter_notifications():
	req = session.post(api_url + "clear_waiter_notifications", json={"waiter_email" : "waiter@waiter.com"})
	if verbose:
		print(req.text)
	return req, req.status_code


# the test are ran in a specific way
# the true/false values correspond to whether it should pass or fail
# true meaning it should pass, and false it should fail
tests = [
		[test_add_waiter_notification, True],
		[test_get_waiter_notifications, True],
		]

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] == "v":
			verbose = True
	total = 0
	passed = 0
	failed = []
	total, passed, failed = tester.run_tests(tests, total, passed, failed)
	tester.print_results(total, passed, failed)








