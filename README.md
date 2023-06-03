# FINAL HANDS-ON (PROCESSES)
In creating this project you must properly installed python in your computer, assuming that you intalled pyhon in your computer 
-Type python --version (to ensure the version of the python in your computer), also make sure that you set up your data base in MySQL Workbench

Make a folder where you want to create this project in your desired path(in my case i created in desktop to easily find my project)
- cd "desktop", mkdir "name of folder", cd "name of the foder"
- Then install virtual environment in the same folder (virtualenv "name of env") then activate the scripts (name of env\scripts\activate)
- Then creat a .gitignore to ignore the env folder
- Initialize the folder (git init)

After that install the necessary modules/ libraries (flask, pip, flask-mysqldb)
- Pip install flask, Pip install flask-mysqldb
- pip freeze to check wheter both of them are successfuly installed
- In another way you can try to create a file like testflask.py and create code to test the flask (in my case i create testflask.py)
- Git add and make a commit

Create an .py (in my case i use api.py) and generate the code
- Make sure you import necessary modules/libraries
- To configure your MySQL Server, make sure that the database configuration in the API script, specifically the values for MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DB, align with the database setup on your local machine. This alignment is crucial as it determines whether you'll be granted access to interact with the database table.

After connecting your data base in python 
- Create a get, post, put, delete methods in your code 
- It will manipulate your data base
- In my case i created testapp.py for my test driven development in a simple approach to secure the code will work properly
- Add some input validation and error handling and add a Generate XML response based on data provided
- I add additional feature where it search request in the data base

Lastly 
- Dont forget to make commit in every method you aadd in your code
- then push it to your repository then clone to your local

NOTE: Make sure the all data especially the data base is connected 
TRY IT AND ENJOY

# OVERVIEW PROCESS OF THE API.PY or the main code
Here is an overview of the process:

- The necessary dependencies are imported, including Flask, jsonify, request, Response, MySQL, datetime, and xml.etree.ElementTree.
- The Flask application is initialized.
- MySQL configurations are set in the app.config object, specifying the host, user, password, database, and cursor class.
- The MySQL connection is established using the MySQL object and the app instance.
- The function generate_xml_response is defined to generate an XML response based on the provided data.
- The function execute_query is defined to execute a query on the MySQL database and return the fetched data.
- A default route is defined to return a simple message.
- The endpoint /dept_emp is defined to handle a GET request, retrieving all department employees from the dept_emp table.
- The endpoint /dept_emp/<int:emp_no> is defined to handle a GET request, retrieving a specific department employee by their employee number.
- The endpoint /dept_emp is defined to handle a POST request, adding a new department employee to the dept_emp table.
- The endpoint /dept_emp/<int:emp_no> is defined to handle a PUT request, updating an existing department employee in the dept_emp table.
- The endpoint /dept_emp/<int:emp_no> is defined to handle a DELETE request, deleting a department employee from the dept_emp table.
- The endpoint /dept_emp/search is defined to handle a GET request, allowing the search for department employees based on employee number and/or department number.
- The application is run when the script is executed.

