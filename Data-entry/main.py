from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)
#Database config, loads from db.yaml
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
#Creates the MySql configuration.
mysql = MySQL(app)

#When you add a route the user can access the corrosponding directory/route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #Gets the form data
        userDetails = request.form
        Username = userDetails['users']
        Fullname = userDetails['name']
        Useremail = userDetails['email']
        Userpassword = userDetails['password']
        cur = mysql.connection.cursor()
        #creates the connection and, passes the user input.
        cur.execute("INSERT INTO USER_INFO(USERNAME, FULLNAME, EMAIL_USER ,USER_PASSWORD) VALUES(%s, %s, %s,%s)",(Username ,Fullname ,Useremail, Userpassword))
        mysql.connection.commit()
        cur.close()
        #returns a message after the data has entered.
        return 'success'
    return render_template('index.html')
@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM USER_INFO")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)
if __name__ == '__main__':
    app.run(debug=True) #Switch this to false when the application goes into production mode.
