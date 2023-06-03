# Imporing process
from flask import Flask, jsonify, request, Response
from flask_mysqldb import MySQL
from datetime import datetime
import xml.etree.ElementTree as ET

app = Flask(__name__)

# MySQL configurations
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "employees"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Connecting to MySQL database
mysql = MySQL(app)


def generate_xml_response(data):
    # Generate XML response based on data provided
    root = ET.Element("dept_emp")

    if isinstance(data, dict):
        employee = ET.SubElement(root, "employee")
        for key, value in data.items():
            ET.SubElement(employee, key).text = str(value)
    elif isinstance(data, list):
        for item in data:
            employee = ET.SubElement(root, "employee")
            for key, value in item.items():
                ET.SubElement(employee, key).text = str(value)
    else:
        # Return error response if data format is invalid
        return Response(response=jsonify({"error": "Invalid data format"}), status=500, mimetype="application/json")

    xml_data = ET.tostring(root).decode()
    return Response(response=xml_data, status=200, mimetype="application/xml")


def execute_query(query, params=None):
    # Execute a query on the MySQL database
    cur = mysql.connection.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/")
def hello_world():
    # Default route that returns a simple message
    return "<p>SOLIS, JOHN PAUL (FINALS)!</p>"

# GET information in the dept_emp table
@app.route("/dept_emp", methods=["GET"])
def get_dept_emp():
    # Get all department employees
    format_param = request.args.get("format", "json")

    query = "SELECT * FROM dept_emp"
    data = execute_query(query)

    if format_param.lower() == "xml":
        # Generate XML response if format is XML
        return generate_xml_response(data)

    return jsonify(data), 200

# GET method by emp_no
@app.route("/dept_emp/<int:emp_no>", methods=["GET"])
def get_dept_emp_by_emp_no(emp_no):
    # Get department employee by employee number
    format_param = request.args.get("format", "json")

    query = "SELECT * FROM dept_emp WHERE emp_no = %s"
    data = execute_query(query, (emp_no,))

    if not data:
        # Return error if department employee is not found
        return jsonify({"error": "No department employee found with the given emp_no"}), 404

    if format_param.lower() == "xml":
        # Generate XML response if format is XML
        return generate_xml_response(data)

    return jsonify(data), 200

# POST method (Add new data)
@app.route("/dept_emp", methods=["POST"])
def add_dept_emp():
    # Add a new department employee
    format_param = request.args.get("format", "json")
    info = request.get_json()

    required_fields = ["emp_no", "dept_no", "from_date", "to_date"]
    if not all(key in info for key in required_fields):
        # Return error if required fields are missing
        return jsonify({"error": "Missing required fields"}), 400

    try:
        from_date = datetime.strptime(info["from_date"], "%a, %d %b %Y %H:%M:%S %Z").date()
        to_date = datetime.strptime(info["to_date"], "%a, %d %b %Y %H:%M:%S %Z").date()
    except ValueError:
        # Return error if date format is invalid
        return jsonify({"error": "Invalid date format"}), 400

    with mysql.connection.cursor() as cur:
        cur.execute("INSERT INTO dept_emp (emp_no, dept_no, from_date, to_date) VALUES (%s, %s, %s, %s)",
                    (info["emp_no"], info["dept_no"], from_date, to_date))
        mysql.connection.commit()
        rows_affected = cur.rowcount

    if format_param.lower() == "xml":
        # Generate XML response if format is XML
        response_data = generate_xml_response({"message": "Department employee added successfully",
                                               "rows_affected": rows_affected})
        return response_data

    response = jsonify({"message": "Department employee added successfully",
                        "rows_affected": rows_affected})
    response.headers["Content-Type"] = "application/json"  # Set the content type explicitly

    return response, 201

# PUT method (update the data)
@app.route("/dept_emp/<int:emp_no>", methods=["PUT"])
def update_dept_emp(emp_no):
    # Update an existing department employee
    format_param = request.args.get("format", "json")
    info = request.get_json()

    required_fields = ["dept_no", "from_date", "to_date"]
    if not all(key in info for key in required_fields):
        # Return error if required fields are missing
        return jsonify({"error": "Missing required fields"}), 400

    try:
        from_date = datetime.strptime(info["from_date"], "%a, %d %b %Y %H:%M:%S %Z").date()
        to_date = datetime.strptime(info["to_date"], "%a, %d %b %Y %H:%M:%S %Z").date()
    except ValueError:
        # Return error if date format is invalid
        return jsonify({"error": "Invalid date format"}), 400

    query = "UPDATE dept_emp SET dept_no = %s, from_date = %s, to_date = %s WHERE emp_no = %s"
    params = (info["dept_no"], from_date, to_date, emp_no)

    with mysql.connection.cursor() as cur:
        cur.execute(query, params)
        mysql.connection.commit()
        rows_affected = cur.rowcount

    if format_param.lower() == "xml":
        # Generate XML response if format is XML
        response_data = generate_xml_response({"message": "Department employee updated successfully",
                                               "rows_affected": rows_affected})
        return response_data

    return jsonify({"message": "Department employee updated successfully",
                    "rows_affected": rows_affected}), 200

# DELETE method (Delete data)
@app.route("/dept_emp/<int:emp_no>", methods=["DELETE"])
def delete_dept_emp(emp_no):
    # Delete a department employee
    format_param = request.args.get("format", "json")

    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM dept_emp WHERE emp_no = %s", (emp_no,))
        mysql.connection.commit()
        rows_affected = cur.rowcount

    if rows_affected == 0:
        # Return error if department employee is not found
        return jsonify({"error": "No department employee found with the given emp_no"}), 404

    if format_param.lower() == "xml":
        # Generate XML response if format is XML
        response_data = generate_xml_response({"message": "Department employee deleted successfully",
                                               "rows_affected": rows_affected})
        return response_data

    return jsonify({"message": "Department employee deleted successfully",
                    "rows_affected": rows_affected}), 200

# Additional feutures where it search in data base
@app.route("/dept_emp/search", methods=["GET"])
def search_dept_emp():
    # Search for department employees based on employee number and/or department number
    format_param = request.args.get("format", "json")

    emp_no = request.args.get("emp_no")
    dept_no = request.args.get("dept_no")

    query = "SELECT * FROM dept_emp WHERE 1=1"
    params = []

    if emp_no:
        query += " AND emp_no = %s"
        params.append(emp_no)
    if dept_no:
        query += " AND dept_no = %s"
        params.append(dept_no)

    data = execute_query(query, tuple(params))

    if format_param.lower() == "xml":
        # Generate XML response if format is XML
        return generate_xml_response(data)

    return jsonify(data), 200


if __name__ == "__main__":
    app.run(debug=True)
