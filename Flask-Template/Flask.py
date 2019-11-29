from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html') #This is a blank html file, you can change it/modify it

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0' ,port=80) #0.0.0.0 = Your IP, you can change it to 127.0.0.1 for local host
