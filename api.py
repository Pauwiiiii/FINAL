from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL


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

if __name__ == "__main__":
    app.run(debug=True)

