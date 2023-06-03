import unittest
import warnings
from api import app

class MyApptests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_get_dept_emp(self):
        response = self.app.get("/dept_emp")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'"dept_no":"d001","emp_no":10001,"from_date":"Thu, 26 May 2005 00:00:00 GMT","to_date":"Sun, 01 May 2005 00:00:00 GMT"' in response.data)

    def test_get_dept_emp_by_emp_no(self):
        response = self.app.get("/dept_emp/10002")
        self.assertEqual(response.status_code, 200)
        data = response.data.decode()  # Decode the response data from bytes to string
        print(data)  # Print response data for debugging
        self.assertTrue("d007" in data)

if __name__ == "__main__":
    unittest.main()
