from flask import Blueprint, render_template, request

# defining blueprint
auth = Blueprint("auth", __name__)

# defining route to login
@auth.route("/login/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("Username = ", username, " Password = ", password)
    return render_template("login.html")