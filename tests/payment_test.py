import requests, json, sys
try:
    from . import tester, session_test
except:
    import tester, session_test

session = requests.Session()
session_test.session = session
session_test.verbose = True

verbose = False

api_url = "http://localhost:5000/"


def test_no_card_num_verify_payment():
    req = session.post(api_url + "verify_payment")
    if verbose:
        print(req.text)
    return req, req.status_code


def test_invalid_card_num_verify_payment():
    req = session.post(api_url + "verify_payment", json={"card_num": "-1",
                                                         "cvv": "123",
                                                         "sort_num": "123456",
                                                         "expiry_date": "1030"
                                                         })
    if verbose:
        print(req.text)
    return req, req.status_code


def test_no_cvv_verify_payment():
    req = session.post(api_url + "verify_payment", json={"card_num": "1"})
    if verbose:
        print(req.text)
    return req, req.status_code


def test_invalid_cvv_verify_payment():
    req = session.post(api_url + "verify_payment", json={"card_num": "123456789123456",
                                                         "cvv": "6",
                                                         "sort_num": "123456",
                                                         "expiry_date": "1030"
                                                         })
    if verbose:
        print(req.text)
    return req, req.status_code


def test_no_sort_num_verify_payment():
    req = session.post(api_url + "verify_payment", json={"card_num": "1", "cvv": "1"})
    if verbose:
        print(req.text)
    return req, req.status_code


def test_invalid_sort_num_verify_payment():
    req = session.post(api_url + "verify_payment", json={"card_num": "123456789123456",
                                                         "cvv": "123",
                                                         "sort_num": "-234",
                                                         "expiry_date": "1030"
                                                         })
    if verbose:
        print(req.text)
    return req, req.status_code


def test_no_expiry_date_verify_payment():
    req = session.post(api_url + "verify_payment", json={"card_num": "1", "cvv": "1", "sort_num": "1"})
    if verbose:
        print(req.text)
    return req, req.status_code


# The expiry date is in the past
def test_expired_expiry_date_verify_payment():
    req = session.post(api_url + "verify_payment", json={"card_num": "123456789123456",
                                                         "cvv": "123",
                                                         "sort_num": "123456",
                                                         "expiry_date": "1015"
                                                         })
    if verbose:
        print(req.text)
    return req, req.status_code


# The expiry date is not in the correct format
def test_invalid_expiry_date_verify_payment():
    req = session.post(api_url + "verify_payment", json={"card_num": "123456789123456",
                                                         "cvv": "123",
                                                         "sort_num": "123456",
                                                         "expiry_date": "10/30"
                                                         })
    if verbose:
        print(req.text)
    return req, req.status_code


def test_verify_payment():
    req = session.post(api_url + "verify_payment", json={"card_num": "123456789123456",
                                                         "cvv": "123",
                                                         "sort_num": "123456",
                                                         "expiry_date": "1030"
                                                         })
    if verbose:
        print(req.text)
    return req, req.status_code


# the test are ran in a specific way
# the true/false values correspond to whether it should pass or fail
# true meaning it should pass, and false it should fail
tests = [
        [test_no_card_num_verify_payment, False],
        [test_invalid_card_num_verify_payment, False],
        [test_no_cvv_verify_payment, False],
        [test_invalid_cvv_verify_payment,False],
        [test_no_sort_num_verify_payment, False],
        [test_invalid_sort_num_verify_payment, False],
        [test_no_expiry_date_verify_payment, False],
        [test_expired_expiry_date_verify_payment, False],
        [test_invalid_expiry_date_verify_payment, False],
        [test_verify_payment, True],
        ]

if __name__ == "__main__":
    total = 0
    passed = 0
    failed = []
    if len(sys.argv) > 1 and sys.argv[1] == "v":
        verbose = True
    total, passed, failed = tester.run_tests(tests, total, passed, failed)
    tester.print_results(total, passed, failed)
