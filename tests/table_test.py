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


def test_get_tables():
    req = session.post(api_url + "get_tables")
    if verbose:
        print(req.text)
    return req, req.status_code


def test_get_tables_and_waiters():
    req = session.post(api_url + "get_tables_and_waiters")
    if verbose:
        print(req.text)
    return req, req.status_code


def test_get_unassigned_tables():
    req = session.post(api_url + "get_unassigned_tables")
    if verbose:
        print(req.text)
    return req, req.status_code


def test_no_waiter_id_table_assignment_event():
    req = session.post(api_url + "table_assignment_event", json={"table_id": "1"})
    if verbose:
        print(req.text)
    return req, req.status_code


def test_invalid_waiter_id_table_assignment_event():
    req = session.post(api_url + "table_assignment_event", json={"waiter_id": "1", "table_id": "1"})
    if verbose:
        print(req.text)
    return req, req.status_code


def test_no_table_id_table_assignment_event():
    req = session.post(api_url + "table_assignment_event", json={"waiter_id": "waiter@waiter.com"})
    if verbose:
        print(req.text)
    return req, req.status_code


def test_invalid_table_id_table_assignment_event():
    req = session.post(api_url + "table_assignment_event", json={"waiter_id": "1", "table_id": "-1"})
    if verbose:
        print(req.text)
    return req, req.status_code


def test_table_assignment_event():
    req = session.post(api_url + "table_assignment_event", json={"waiter_id": "waiter@waiter.com", "table_id": "1"})
    if verbose:
        print(req.text)
    return req, req.status_code


def test_no_table_id_get_waiter_assigned_to_table():
    req = session.post(api_url + "get_waiter_assigned_to_table", json={})
    if verbose:
        print(req.text)
    return req, req.status_code


def test_invalid_table_id_get_waiter_assigned_to_table():
    req = session.post(api_url + "get_waiter_assigned_to_table", json={"table_id": "-1"})
    if verbose:
        print(req.text)
    return req, req.status_code


def test_get_waiter_assigned_to_table():
    req = session.post(api_url + "get_waiter_assigned_to_table", json={"table_id": "1"})
    if verbose:
        print(req.text)
    return req, req.status_code


# the test are ran in a specific way
# the true/false values correspond to whether it should pass or fail
# true meaning it should pass, and false it should fail
tests = [
        [test_get_tables, True],
        [test_get_tables_and_waiters, True],
        [test_get_unassigned_tables, True],
        [test_no_waiter_id_table_assignment_event, False],
        [test_invalid_waiter_id_table_assignment_event, False],
        [test_no_table_id_table_assignment_event, False],
        [test_invalid_table_id_table_assignment_event, False],
        [test_table_assignment_event, True],
        [test_no_table_id_get_waiter_assigned_to_table, False],
        [test_invalid_table_id_get_waiter_assigned_to_table, False],
        [test_get_waiter_assigned_to_table, True],
        ]

if __name__ == "__main__":
    total = 0
    passed = 0
    failed = []
    if len(sys.argv) > 1 and sys.argv[1] == "v":
        verbose = True
    total, passed, failed = tester.run_tests(tests, total, passed, failed)
    tester.print_results(total, passed, failed)
