import requests, json, sys
try:
	from . import tester
except:
	import tester

session = requests.Session()

verbose = False

api_url = "http://localhost:5000/"

def test_get_menu():
	req = session.post(api_url + "menu")
	if verbose:
		print(req.text)
	return req, req.status_code
	

# TODO add tests for selecting specific menu groups (allergy etc.)

# the test are ran in a specific way
# the true/false values correspond to whether it should pass or fail
# true meaning it should pass, and false it should fail
tests = [
		[test_get_menu, True],
		]

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] == "v":
		verbose = True
	total = 0
	passed = 0
	failed = []
	total, passed, failed = tester.run_tests(tests, total, passed, failed)
	tester.print_results(total, passed, failed)

