from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
app = Flask(__name__)
crypt = Bcrypt(app)
app.config['MONGO_DBNAME'] = 'MONGODB_NAME'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/MONGODB_NAME'
mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'Hello ' + session['username']
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if  (crypt.check_password_hash(login_user['password'], request.form['pass'])):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password': crypt.generate_password_hash(request.form['password'])})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'The username you have chosen already exists.'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
