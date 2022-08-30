from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User

@app.route("/") #--> Enter new users
def index():
    return render_template("form.html")
            
@app.route('/show_all_users') #--> Users table
def show_user_table():
    users = User.get_all()
    print(users)
    return render_template("users.html", all_users = users)

@app.route('/show_details/<int:user_id>') #--> Show user details
def show_user_details(user_id):
    users = User.get_all()
    user_profile = {}
    for user in users:
        if user.id == user_id:
            user_profile = user
    return render_template("details.html", user = user_profile)

@app.route('/edit/<int:user_id>') #--> Edit user details
def edit_user_details(user_id):
    users = User.get_all()
    user_profile = {}
    for user in users:
        if user.id == user_id:
            user_profile = user
    return render_template("edit.html", user = user_profile)

@app.route('/create_user', methods=["POST"]) #--> Users created
def create_user():
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email": request.form["email"]
    }
    if not User.validate_user(data):
        # we redirect to the template with the form.
        return redirect('/')
    User.save(data)
    return redirect('/show_all_users')

@app.route('/update_user/<int:user_id>', methods=["POST"]) #--> Users updated
def update_user(user_id):
    users = User.get_all()
    user_instance = None
    for user in users:
        if user.id == user_id:
            user_instance = user
    data = {
        "first_name": request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email": request.form['email'],
        "id": user_id
    }
    print("HEREEEE")
    print(data)
    User.update(data)
    return redirect('/show_all_users')

@app.route('/delete/<int:user_id>') #--> User deleted
def delete_user(user_id):
    data = {
        "id": user_id
    }
    User.delete(data)
    print(data)
    return redirect('/show_all_users')