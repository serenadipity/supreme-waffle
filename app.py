from flask import Flask, render_template, request, session, redirect, url_for

from datas import *

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    return render_template("home.html", user = user)

@app.route("/about")
def about():
    if 'user' not in session:
        session['user'] = "0"
    user = session['user']
    return render_template("about.html", user = user)

@app.route("/create", methods=['GET','POST'])
def create():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if request.method == "GET":
        return render_template("create.html", user=user)
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
            return render_template("create.html",user = user, error = True, message = message)

@app.route("/login", methods=['GET','POST'])
def login():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if request.method == "GET":
        return render_template("login.html", user=user)
    else:
        username = request.form['username']
        password = request.form['password']
        result = authenticate(username, password)
        if result != -1:
            session['user'] = username
            return redirect("home")
        else:
            return render_template("login.html", user = user, error = True)

@app.route("/logout")
def logout():
    session['user'] = 0
    return redirect("home")

@app.route("/register_school", methods=['GET','POST'])
def register_school():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if request.method == "GET":
        return render_template("register_school.html", user=user)
    else:
        school_name = get_user_school(user)
        street_address = request.form['street_address']
        borough = request.form['borough']
        zipcode = request.form['zipcode']
        team = request.form['team']
        division = request.form['division']
        coach = request.form['coach']
        manager = request.form['manager']
        gender = request.form['gender']
        result = create_school(school_name, street_address, borough, zipcode, team, division, coach, manager, gender)
        if result[0] == False:
            return redirect("school.html", school = school_name)
        else:
            return render_template("register_school.html", user = user, error = True, message = result[1])
    return "success"

@app.route("/register_player", methods=['GET','POST'])
def register_player():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if request.method == "GET":
        return render_template("register_player.html", user=user)
    else:
        year = request.form['year']
        first_name = request.form['fname']
        last_name = request.form['lname']
        school = get_user_school(user)
        gender = request.form['gender']
        grad_year = request.form['grad_year']
        player_type = request.form['player_type']
        matches = request.form['matches']
        win = request.form['win']
        loss = request.form['loss']
        touch = request.form['touch']
        position = request.form['position']
        result = create_player(year, first_name, last_name, school, gender, grad_year, player_type, matches, win, loss, touch, position)
        print "SUCCES"
        if result[0] == False:
            return redirect("player.html", player_id = player_id)
        else:
            return render_template("register_player.html", error = True, message = result[1])


@app.route("/school/<school>")
def show_school_profile(school):
    result = get_school(school)
    return render_template("school.html", error = result[0], data = result[1]) 

@app.route("/player/<player>")
def show_player_profile(player):
    #look up player
    return render_template("player.html") #add some params

@app.route("/directory")
def default_directory():
    return redirect("directory/A")

@app.route("/directory/<letter>")
def display_directory(letter):
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    return render_template("letter.html", letter = letter, user = user) #add some params

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "Password"
    app.run(host='0.0.0.0', port=8000)
