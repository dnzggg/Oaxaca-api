import json


def run_tests(test_array, total, passed, failed):
	total += len(test_array)
	for [test, should_pass] in test_array:
		print("\n\033[93mRUNNING TEST: " + test.__name__.upper() + "...\033[0m")
		request, code = test()
		if code // 100 == 2 or code // 100 == 3:
			print("\033[92mSUCCESSFUL REQUEST, HTML STATUS CODE:" + str(code) + "\033[0m")
			if should_pass is None:  # this is when the test just tests if the api is up, a ping request
				passed += 1

			elif not should_pass and "error" not in request.json():  # if there is supposed to be an error message but none found
				failed.append(test.__name__.upper())

			elif should_pass and "data" not in request.json():  # if there is supposed to be data but none found
				failed.append(test.__name__.upper())

			else:  # The message returned was correct
				passed += 1
		else:
			print("\033[91mUNSUCCESSFUL REQUEST, HTML STATUS CODE:" + str(code) + "\033[0m")
			failed.append(test.__name__.upper())

	return total, passed, failed


def print_results(total, passed, failed):
	print("Total Tests: {}".format(total))
	print("\033[92mTotal Passed: {}\033[0m".format(passed))
	if len(failed) != 0:
		print("\033[91mTotal Failed: {}\033[0m".format(len(failed)))
		for i in range(len(failed)):
			print("\033[91m\t{}. Test {} Failed\033[0m".format(i + 1, failed[i]))
	else:
		print("\033[92mAll tests Passed!!\033[0m")
