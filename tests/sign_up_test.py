import requests, sys

try:
    from . import tester, session_test
except:
    import tester, session_test
sys.path.append("../")
from common import connector


session = requests.Session()
session_test.session = session
session_test.verbose = True

verbose = False

user_data = {
    "email": "test@user.com",
    "firstname": "Test",
    "lastname": "User",
    "password": "password",
    "staff_login": False
}

staff_data = {
    "email": "test@waiter.com",
    "firstname": "Test",
    "lastname": "Waiter",
    "phone_number": "07123456789",
    "password": "password",
    "staff_login": True
}

api_url = "http://localhost:5000/"


################################
#### Customer sign up tests ####
################################


def test_no_input_sign_up():
    req = session.post(api_url + "signup")
    if verbose:
        print(req.text)
    return req, req.status_code


def test_in_use_email():
    bad_user_data = user_data
    bad_user_data["email"] = "example@example.com"
    req = session.post(api_url + "signup", json=bad_user_data)
    if verbose:
        print(req.text)
    return req, req.status_code


def test_user_sign_up():
    user_data["email"] = "test@user.com"
    req = session.post(api_url + "signup", json=user_data)
    if verbose:
        print(req.text)
    return req, req.status_code


def test_login_before_signup():
    req = session.post(api_url + "login", json=user_data)
    if verbose:
        print(req.text)
    return req, req.status_code


def test_login_after_signup():
    req = session.post(api_url + "login", json=user_data)
    if verbose:
        print(req.text)
    cleanup_customer()
    return req, req.status_code

##############################
#### Waiter sign up tests ####
##############################


def test_no_input_staff_sign_up():
    req = session.post(api_url + "waiter_signup")
    if verbose:
        print(req.text)
    return req, req.status_code


def test_in_use_staff_email():
    bad_user_data = user_data
    bad_user_data["email"] = "waiter@waiter.com"
    req = session.post(api_url + "waiter_signup", json=bad_user_data)
    if verbose:
        print(req.text)
    return req, req.status_code


def test_staff_sign_up():
    req = session.post(api_url + "waiter_signup", json=staff_data)
    if verbose:
        print(req.text)
    return req, req.status_code


def test_staff_login_before_signup():
    req = session.post(api_url + "login", json=staff_data)
    if verbose:
        print(req.text)
    return req, req.status_code


def test_staff_login_after_signup():
    req = session.post(api_url + "login", json=staff_data)
    if verbose:
        print(req.text)
    cleanup_waiter()
    return req, req.status_code


def cleanup_customer():
    connector.execute_insert_query("DELETE FROM customer WHERE email = 'test@user.com'")


def cleanup_waiter():
    connector.execute_insert_query("DELETE FROM waiter WHERE email = 'test@waiter.com'")

# the test are ran in a specific way
# the true/false values correspond to whether it should pass or fail
# true meaning it should pass, and false it should fail
tests = [
    [test_no_input_sign_up, False],
    [test_in_use_email, False],
    [test_login_before_signup, False],
    [test_user_sign_up, True],
    [test_login_after_signup, True],
    [test_staff_login_before_signup, False],
    [test_staff_sign_up, True],
    [test_staff_login_after_signup, True],
]

if __name__ == "__main__":
    total = 0
    passed = 0
    failed = []
    if len(sys.argv) > 1 and sys.argv[1] == "v":
        verbose = True
    total, passed, failed = tester.run_tests(tests, total, passed, failed)
    tester.print_results(total, passed, failed)
