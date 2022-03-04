from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.round import Round
from flask_app.models.user import User

# DISPLAY

@app.route('/rounds/new')
def new_rounds():
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id": session["user_id"]
    }
    user = User.get_by_id(data)
    return render_template("round_new.html", user = user)

# Update rounds on display
@app.route('/rounds/<int:id>/edit')
def update_round(id):
    if 'user_id' not in session:
        return redirect ("/")
    
    data = {
        "id":id
    }

    data1 = {
        "id": session["user_id"]
    }
    user = User.get_by_id(data1)

    round = Round.get_one(data)
    print(round.course_name)
    return render_template("round_edit.html", round = round, user = user)

# Show rounds
@app.route('/rounds/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect ("/")

    data = {
        "id": session["user_id"]
    }

    data1 = {
        "id" : id
    }
    user = User.get_by_id(data)
    round = Round.get_one(data1)

    if not round:
        return redirect ("/dashboard")

    return render_template("round_show.html", round = round, user = user,)

# ACTION

# Create round

@app.route('/rounds/create', methods = ['POST'])
def create_round():

    if not Round.is_valid(request.form):
        return redirect('/rounds/new')
    print(request.form)
    data = {
        "course_name" : request.form["course_name"],
        "tee_time" : request.form["tee_time"],
        "description" : request.form["description"],
        "user_id" : session["user_id"]

    }

    Round.save(data)

    return redirect("/plans")

# Update round

@app.route('/rounds/update', methods = ['POST'])
def change():
    if not Round.is_valid(request.form):
        return redirect(f'/rounds/{request.form["id"]}/edit')
    print(request.form)
    Round.update(request.form)
    return redirect ("/plans")           

# Delete painting

@app.route('/rounds/delete/<int:id>')
def delete(id):
    data = {
        "id":id
    }
    Round.destroy(data)
    return redirect ("/dashboard")  