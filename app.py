from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

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

@app.route("directory/<letter>")
def display_directory(letter):
    return render_template("letter.html") #add some params

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "Password"
    app.run(host='0.0.0.0', port=8000)
