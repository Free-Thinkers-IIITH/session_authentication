import re
from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database('ssd')
records = db.login_credentials

@app.route("/")
def landing_page():
    msg = " "
    if "email" in session:
        msg = session["email"]
    return render_template("landingpage.html", message = msg)

@app.route("/logged_in")
def check_logged_in():
    if "email" in session:
        return render_template("logged_in.html", email = session["email"])
    else:
        return render_template("login_page.html")
@app.route("/register")
def login():
    if "email" in session:
         return render_template("landingpage.html")
    user_input = {"Name":"Aakash","LastName":"Singh"}
    #records.insert_one(user_input)
    return render_template("register.html")

@app.route("/login")
def login_here():
    return render_template('login_page.html')

@app.route("/logging_in",  methods=['post', 'get'])
def log_user_in():
    if "email" in session:
        return render_template("landingpage.html")
    message = 'Please login to your account'

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pwd")

       
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('check_logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login_page.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login_page.html', message=message)
    return render_template('login_page.html', message=message)

@app.route("/register_in", methods=['post', 'get'])
def index():
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fname")
        email = request.form.get("email")
        
        password1 = request.form.get("pwd")
        
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
        user_input = {'name': user, 'email': email, 'password': hashed}
        records.insert_one(user_input)
            
        user_data = records.find_one({"email": email})
        new_email = user_data['email']
   
        return render_template('logged_in.html', email=new_email)
    return render_template('register.html')

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("register.html")

#end of code to run it
if __name__ == "__main__":
  app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
