from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "employees"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

#Coonecting to mysql app
mysql = MySQL(app)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Refractor of code
def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


# Display query from employees data base and get from web application
@app.route("/dept_emp", methods=["GET"])
def get_dept_emp():
    # cur = mysql.connection.cursor()
    data = data_fetch("""SELECT * FROM dept_emp""")
    return make_response(jsonify(data), 200)
    # query = """
    #select * from dept_emp w
    #"""
    # '''cur.execute(query)
    # data = cur.fetchall()
    # cur.close() ''' 
 
    

# New function before refractor
@app.route("/dept_emp/<int:emp_no>", methods=["GET"])
def get_dept_emp_by_emp_no(emp_no):
    # cur =mysql.connection.cursor()
    data = data_fetch("""select * from dept_emp where emp_no = {}""".format(emp_no))
    return make_response(jsonify(data), 200)
    # query = """
    # select * from dept_emp where emp_no = {}
    # """.format(emp_no)
    # cur.execute(query)
    # data = cur.fetchall()
    # cur.close()

# POST method
@app.route("/dept_emp", methods=["POST"])
def add_dept_emp():
    cur = mysql.connection.cursor()
    info = request.get_json()
    
    # Values
    emp_no = info["emp_no"] # Make sure the emp_no is exist in data base
    dept_no = info["dept_no"]
    from_date_str = info["from_date"]
    to_date_str = info["to_date"]
    
    # Convert date strings to datetime objects
    from_date = datetime.strptime(from_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
    to_date = datetime.strptime(to_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
    
    cur.execute("INSERT INTO dept_emp (emp_no, dept_no, from_date, to_date) VALUES (%s, %s, %s, %s)", (emp_no, dept_no, from_date, to_date))
    mysql.connection.commit()
    
    rows_affected = cur.rowcount 
    cur.close()
    
    return make_response(jsonify({"Message": "Department employee added successfully", "rows_affected": rows_affected}), 201)

# UPDATE METHOD(PUT)
@app.route("/dept_emp/<int:emp_no>", methods=["PUT"])
def update_dept_emp(emp_no):
    cur = mysql.connection.cursor()
    info = request.get_json()
    # Values
    # emp_no = info["emp_no"] 
    dept_no = info["dept_no"] # Make sure the dept_no is exist in data base
    from_date_str = info["from_date"]
    to_date_str = info["to_date"]
    
    # Convert date strings to datetime objects
    from_date = datetime.strptime(from_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()
    to_date = datetime.strptime(to_date_str, "%a, %d %b %Y %H:%M:%S %Z").date()

    cur.execute(""" UPDATE dept_emp SET dept_no = %s, from_date = %s, to_date = %s where emp_no = %s  """, (dept_no, from_date, to_date, emp_no))
    mysql.connection.commit()
    
    rows_affected = cur.rowcount 
    cur.close()
    
    return make_response(jsonify({"Message": "Department employee updated successfully", "rows_affected": rows_affected}), 200)

if __name__ == "__main__":
    app.run(debug=True)
    app.run(debug=True)