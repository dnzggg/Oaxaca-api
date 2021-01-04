from . import login_test, session_test, menu_test, order_test, notification_test, table_test, payment_test, sign_up_test
from . import tester
import sys


if len(sys.argv) > 1 and sys.argv[1] == "v":
	login_test.verbose = True
	session_test.verbose = True
	menu_test.verbose = True
	order_test.verbose = True
	notification_test.verbose = True

all_tests = [
			login_test,
			session_test,
			menu_test,
			order_test,
			notification_test,
			table_test,
			payment_test,
			sign_up_test
			]

total = 0
passed = 0
failed = []

for test in all_tests:
	total, passed, failed = tester.run_tests(test.tests, total, passed, failed)

tester.print_results(total, passed, failed)

