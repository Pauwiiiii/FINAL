from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "employees"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Connecting to MySQL database
mysql = MySQL(app)


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


# Get Method for dept_emp table
@app.route("/dept_emp", methods=["GET"])
def get_dept_emp():
    query = "SELECT * FROM dept_emp"
    data = data_fetch(query)
    return make_response(jsonify(data), 200)


# Get method for dept_emp using the emp_no
@app.route("/dept_emp/<int:emp_no>", methods=["GET"])
def get_dept_emp_by_emp_no(emp_no):
    query = "SELECT * FROM dept_emp WHERE emp_no = %s"
    data = data_fetch(query, (emp_no,))
    
    if not data:
        return make_response(jsonify({"error": "No department employee found with the given emp_no"}), 404)
    
    return make_response(jsonify(data), 200)


# Post Method 
@app.route("/dept_emp", methods=["POST"])
def add_dept_emp():
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

    return make_response(jsonify({"message": "Department employee added successfully",
                                   "rows_affected": rows_affected}), 201)


# Put method (update)
@app.route("/dept_emp/<int:emp_no>", methods=["PUT"])
def update_dept_emp(emp_no):
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

    return make_response(jsonify({"message": "Department employee updated successfully",
                                   "rows_affected": rows_affected}), 200)


# Delete method for the dept_emp table
@app.route("/dept_emp/<int:emp_no>", methods=["DELETE"])
def del_dept_emp(emp_no):
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM dept_emp WHERE emp_no = %s", (emp_no,))
        mysql.connection.commit()
        rows_affected = cur.rowcount

    if rows_affected == 0:
        return make_response(jsonify({"error": "No department employee found with the given emp_no"}), 404)

    return make_response(jsonify({"message": "Dept_emp deleted successfully",
                                   "rows_affected": rows_affected}), 200)


if __name__ == "__main__":
    app.run(debug=True)
