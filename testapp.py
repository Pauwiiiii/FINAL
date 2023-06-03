import unittest
import warnings
import json
from api import app


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

        # Filter and ignore DeprecationWarnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)

    def test_get_dept_emp(self):
        response = self.app.get("/dept_emp")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_get_dept_emp_by_emp_no(self):
        emp_no = 10001  # Replace with an existing emp_no from your dept_emp table
        response = self.app.get(f"/dept_emp/{emp_no}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")

    def test_get_dept_emp_by_emp_no_not_found(self):
        emp_no = 9999
        response = self.app.get(f"/dept_emp/{emp_no}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")

    def test_add_dept_emp(self):
        data = {
            "emp_no": 10909,  # Replace with a unique emp_no value
            "dept_no": "d001",
            "from_date": "Mon, 01 Jan 2001 00:00:00 GMT",
            "to_date": "Mon, 01 Jan 2002 00:00:00 GMT"
        }
        response = self.app.post("/dept_emp", json=data)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    def test_update_dept_emp(self):
        emp_no = 10002
        data = {
            "dept_no": "d002",
            "from_date": "Mon, 01 Jan 2003 00:00:00 GMT",
            "to_date": "Mon, 01 Jan 2004 00:00:00 GMT"
        }
        response = self.app.put(f"/dept_emp/{emp_no}", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_delete_dept_emp(self):
        emp_no = 10001
        response = self.app.delete(f"/dept_emp/{emp_no}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")

    def test_delete_dept_emp_not_found(self):
        emp_no = 9999
        response = self.app.delete(f"/dept_emp/{emp_no}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")

    def test_search_dept_emp(self):
        query_params = {
            "emp_no": 10001,
            "dept_no": "d001"
        }
        response = self.app.get("/dept_emp/search", query_string=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_search_dept_emp_no_results(self):
        query_params = {
            "emp_no": 9999
        }
        response = self.app.get("/dept_emp/search", query_string=query_params)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")


if __name__ == "__main__":
    unittest.main()
