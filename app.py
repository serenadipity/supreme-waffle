from flask import Flask, render_template, request, session, redirect, url_for

from datas import register

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/create", methods=['GET','POST'])
def create():
    if request.method == "GET":
        pass
    else:
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        school_name = request.form['school_name']
        result = register(username, password, repeat_password, school_name)
        if result[0]:
            session['user'] = username;
            return redirect("home")
        else:
            message = result[1]
            return render_template("create.html",error = True, message = message)
    return render_template("create.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return url_for("home")

@app.route("/school/<school>")
def show_school_profile(school):
    #look up school
    return render_template("school.html") #add some more params

@app.route("/plater/<player>")
def show_player_profile(player):
    #look up player
    return render_template("player.html") #add some params

@app.route("/directory/<letter>")
def display_directory(letter):
    return render_template("letter.html") #add some params

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "Password"
    app.run(host='0.0.0.0', port=8000)
