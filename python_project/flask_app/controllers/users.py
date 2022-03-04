from flask import render_template, redirect, request, session
from flask_app import app

from flask_app.models.user import User
from flask_app.models.round import Round
from flask_app.models.profile import Profile


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect ("/dashboard")
    return render_template("home.html")

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect ("/dashboard")
    return render_template("login.html")

@app.route('/create')
def create():
    if 'user_id' in session:
        return redirect ("/dashboard")
    return render_template("create.html")

@app.route('/account')
def account():
    if 'user_id' in session:
        return redirect ("/dashboard")
    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id" : session ["user_id"]
    }
    

    user = User.get_by_id(data)

    rounds = Round.get_all()

    users = User.get_plans_for_user(data)

    profile = Profile.get_one(data)

    return render_template("dashboard.html", user = user, users = users, rounds = rounds, profile = profile)

@app.route('/plans')
def courses():
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id" : session ["user_id"]
    }

    user = User.get_by_id(data)

    users = User.get_plans_for_user(data)

    return render_template("plans.html", user = user, users = users)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id" : session ["user_id"]
    }

    user = User.get_by_id(data)

    users = User.get_plans_for_user(data)

    profile = Profile.get_one(data)

    return render_template("profile.html", profile = profile, user = user, users = users)




# ACTION

@app.route('/createaccount', methods = ['POST'])
def create_account():
    if not User.is_valid(request.form):
        return redirect('/create')

    user_id = User.save(request.form)

    # Using session to keep user logged in
    session['user_id'] = user_id



    return redirect("/dashboard")

# login

@app.route('/loginaccount', methods = ['POST'])
def login_account():
    data = {
        "email" : request.form["email"]
    }
    if User.validate_login(request.form):
        user = User.get_by_email(data)
        session['user_id'] = user.id
        return redirect("/dashboard")
    else:
        return redirect("/account")

# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

