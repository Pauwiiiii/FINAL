# Flask API for interacting with a MySQL database table #dept_emp.
# Includes various endpoints for retrieving, adding, updating, and deleting records.
# Supports both JSON and XML response formats.

from flask import Flask, make_response, jsonify, request, Response
from flask_mysqldb import MySQL
from datetime import datetime
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "employees"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Connecting to MySQL database
mysql = MySQL(app)

# Root route
@app.route("/")
def hello_world():
    return "<p>SOLIS, JOHN PAUL (FINALS)!</p>"

# Utility function to fetch data from MySQL
def data_fetch(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    return data

# Function to generate XML response
def generate_xml_response(data):
    root = ET.Element("dept_emp")
    for item in data:
        employee = ET.SubElement(root, "employee")
        for key, value in item.items():
            ET.SubElement(employee, key).text = str(value)
    xml_data = ET.tostring(root).decode()
    return xml_data

# Get Method for dept_emp table
@app.route("/dept_emp", methods=["GET"])
def get_dept_emp():
    format_param = request.args.get("format", "json")

    query = "SELECT * FROM dept_emp"
    data = data_fetch(query)

    if format_param.lower() == "xml":
        xml_data = generate_xml_response(data)
        return Response(xml_data, mimetype="application/xml")

    return make_response(jsonify(data), 200)

# Get method for dept_emp using the emp_no
@app.route("/dept_emp/<int:emp_no>", methods=["GET"])
def get_dept_emp_by_emp_no(emp_no):
    format_param = request.args.get("format", "json")

    query = "SELECT * FROM dept_emp WHERE emp_no = %s"
    data = data_fetch(query, (emp_no,))

    if not data:
        return make_response(jsonify({"error": "No department employee found with the given emp_no"}), 404)

    if format_param.lower() == "xml":
        xml_data = generate_xml_response(data)
        return Response(xml_data, mimetype="application/xml")

    return make_response(jsonify(data), 200)

# Post Method
@app.route("/dept_emp", methods=["POST"])
def add_dept_emp():
    format_param = request.args.get("format", "json")

    info = request.get_json()

    if not all(key in info for key in ["emp_no", "dept_no", "from_date", "to_date"]):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    emp_no = info["emp_no"]
    dept_no = info["dept_no"]
    from_date_str = info["from_date"]
    to_date_str = info["to_date"]

    try:
        from_date = datetime.strptime(from_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
        to_date = datetime.strptime(to_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
    except ValueError:
        return make_response(jsonify({"error": "Invalid date format"}), 400)

    with mysql.connection.cursor() as cur:
        cur.execute("INSERT INTO dept_emp (emp_no, dept_no, from_date, to_date) VALUES (%s, %s, %s, %s)",
                    (emp_no, dept_no, from_date, to_date))
        mysql.connection.commit()
        rows_affected = cur.rowcount

    if format_param.lower() == "xml":
        response_data = generate_xml_response({"message": "Department employee added successfully",
                                               "rows_affected": rows_affected})
        return Response(response_data, mimetype="application/xml")

    return make_response(jsonify({"message": "Department employee added successfully",
                                   "rows_affected": rows_affected}), 201)

# Put method (update)
@app.route("/dept_emp/<int:emp_no>", methods=["PUT"])
def update_dept_emp(emp_no):
    format_param = request.args.get("format", "json")

    info = request.get_json()

    if not all(key in info for key in ["dept_no", "from_date", "to_date"]):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    dept_no = info["dept_no"]
    from_date_str = info["from_date"]
    to_date_str = info["to_date"]

    try:
        from_date = datetime.strptime(from_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
        to_date = datetime.strptime(to_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
    except ValueError:
        return make_response(jsonify({"error": "Invalid date format"}), 400)

    query = "UPDATE dept_emp SET dept_no = %s, from_date = %s, to_date = %s WHERE emp_no = %s"
    params = (dept_no, from_date, to_date, emp_no)

    with mysql.connection.cursor() as cur:
        cur.execute(query, params)
        mysql.connection.commit()
        rows_affected = cur.rowcount

    if format_param.lower() == "xml":
        response_data = generate_xml_response({"message": "Department employee updated successfully",
                                               "rows_affected": rows_affected})
        return Response(response_data, mimetype="application/xml")

    return make_response(jsonify({"message": "Department employee updated successfully",
                                   "rows_affected": rows_affected}), 200)

# Delete method for the dept_emp table
@app.route("/dept_emp/<int:emp_no>", methods=["DELETE"])
def del_dept_emp(emp_no):
    format_param = request.args.get("format", "json")

    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM dept_emp WHERE emp_no = %s", (emp_no,))
        mysql.connection.commit()
        rows_affected = cur.rowcount

    if rows_affected == 0:
        return make_response(jsonify({"error": "No department employee found with the given emp_no"}), 404)

    if format_param.lower() == "xml":
        response_data = generate_xml_response({"message": "Dept_emp deleted successfully",
                                               "rows_affected": rows_affected})
        return Response(response_data, mimetype="application/xml")

    return make_response(jsonify({"message": "Dept_emp deleted successfully",
                                   "rows_affected": rows_affected}), 200)

if __name__ == "__main__":
    app.run(debug=True)
