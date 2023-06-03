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

# Refracted code
def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

# Get Method for dept_table
@app.route("/dept_emp", methods=["GET"])
def get_dept_emp():
    data = data_fetch("SELECT * FROM dept_emp")
    return make_response(jsonify(data), 200)

# Get method for dept_method using the emp_no
@app.route("/dept_emp/<int:emp_no>", methods=["GET"])
def get_dept_emp_by_emp_no(emp_no):
    query = "SELECT * FROM dept_emp WHERE emp_no = {}".format(emp_no)
    data = data_fetch(query)
    return make_response(jsonify(data), 200)

# Post Method 
@app.route("/dept_emp", methods=["POST"])
def add_dept_emp():
    info = request.get_json()

    emp_no = info["emp_no"]
    dept_no = info["dept_no"]
    from_date_str = info["from_date"]
    to_date_str = info["to_date"]

    from_date = datetime.strptime(from_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
    to_date = datetime.strptime(to_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()

    with mysql.connection.cursor() as cur:
        cur.execute("INSERT INTO dept_emp (emp_no, dept_no, from_date, to_date) VALUES (%s, %s, %s, %s)",
                    (emp_no, dept_no, from_date, to_date))
        mysql.connection.commit()
        rows_affected = cur.rowcount

    return make_response(jsonify({"Message": "Department employee added successfully",
                                   "rows_affected": rows_affected}), 201)


# Put method (update)
@app.route("/dept_emp/<int:emp_no>", methods=["PUT"])
def update_dept_emp(emp_no):
    info = request.get_json()

    dept_no = info["dept_no"]
    from_date_str = info["from_date"]
    to_date_str = info["to_date"]

    from_date = datetime.strptime(from_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
    to_date = datetime.strptime(to_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()

    with mysql.connection.cursor() as cur:
        cur.execute("UPDATE dept_emp SET dept_no = %s, from_date = %s, to_date = %s WHERE emp_no = %s",
                    (dept_no, from_date, to_date, emp_no))
        mysql.connection.commit()
        rows_affected = cur.rowcount

    return make_response(jsonify({"Message": "Department employee updated successfully",
                                   "rows_affected": rows_affected}), 200)

# Delete method for the dept_emp table
@app.route("/dept_emp/<int:emp_no>", methods=["DELETE"])
def del_dept_emp(emp_no):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM dept_emp WHERE emp_no = %s""", (emp_no,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Dept_emp deleted successfully", "rows_affected": rows_affected}), 200)


if __name__ == "__main__":
    app.run(debug=True)
