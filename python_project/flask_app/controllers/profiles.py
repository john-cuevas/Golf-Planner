from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.profile import Profile
from flask_app.models.user import User

# DISPLAY

@app.route('/profile/new')
def new_paintings():
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id": session["user_id"]
    }
    user = User.get_by_id(data)    
    return render_template("profile_new.html", user = user)

# Update profile on display
@app.route('/profile/<int:id>/edit')
def update_profile(id):
    if 'user_id' not in session:
        return redirect ("/")
    
    data = {
        "id":id
    }

    data1 = {
        "id": session["user_id"]
    }
    user = User.get_by_id(data1)    

    profile = Profile.get_one(data)
    return render_template("profile_edit.html", profile = profile, user = user)

# Show profile
@app.route('/profile/<int:id>')
def show_profile(id):
    if 'user_id' not in session:
        return redirect ("/")

    data = {
        "id": session["user_id"]
    }

    data1 = {
        "id" : id
    }
    user = User.get_by_id(data)
    profile = Profile.get_one(data1)

    if not profile:
        return redirect ("/dashboard")

    return render_template("profile_show.html", profile = profile, user = user,)


# ACTION

# Create profile

@app.route('/profile/create', methods = ['POST'])
def create_profile():

    if not Profile.is_valid(request.form):
        return redirect('/profile/new')
    print(request.form)
    data = {
        "age" : request.form["age"],
        "headline" : request.form["headline"],
        "description" : request.form["description"],
        "handicap" : request.form["handicap"],
        "user_id" : session["user_id"]

    }

    Profile.save(data)

    return redirect("/profile")

# Update profile

@app.route('/profile/edit', methods = ['POST'])
def update():
    if not Profile.is_valid(request.form):
        return redirect(f'/profile/{request.form["id"]}/edit')
    print(request.form)
    Profile.update(request.form)
    return redirect ("/profile")           

