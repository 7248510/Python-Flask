from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
app = Flask(__name__)
crypt = Bcrypt(app)
app.config['MONGO_DBNAME'] = 'mongologin3'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mongologin3'
mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'Hello ' + session['username']
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.collection.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if  (crypt.check_password_hash(login_user['password'], request.form['pass'])):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users.collection
        existing_user = users.collection.find_one({'name' : request.form['username']})

        if existing_user is None:
            #hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password': crypt.generate_password_hash(request.form['password'])})
            #users.insert({inc: "_id":0 }'name' : request.form['username'], 'password': crypt.generate_password_hash(request.form['password'])})
            #users.insert({"_id":getNextSequenceValue("user_id"),'name' : request.form['username'], 'password': crypt.generate_password_hash(request.form['password'])})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')

#db.createCollection("uniq_id")
#db.uniq_id.insert({_id:"user_id",sequence_value:0})

#users.insert({"_id":getNextSequenceValue("user_id"),'name' : request.form['username'], 'password': crypt.generate_password_hash(request.form['password'])})
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
