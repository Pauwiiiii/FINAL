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


@app.route("/dept_emp", methods=["GET"])
def get_dept_empt():
    cur =mysql.connection.cursor()
    query = """
    select * from dept_emp
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()

    return make_response(jsonify(data), 200)



def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True)

