from flask import Flask, render_template, request, session, redirect, url_for
import os
from werkzeug import secure_filename

from datas import *

#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')

ALLOWED_EXTENSIONS = set(['png','jpeg','jpg','gif'])

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
        
        if not request.files.get('file', None):
            pass
        elif result[0] == False:
            file = request.files['file']
            if file and ('.' in file.filename and file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS):
                if not secure_filename(file.filename):
                    return render_template("register_school.html", user = user, error = True, message = "Please upload a secure file.")
                else:
                    filename = school_name + "_" + gender + "." + file.filename.rsplit(".",1)[1]
                    filename = "_".join(filename.split(" "))
                file.save(os.path.join("static/school/images/", filename))
                add_school_image(school_name, gender, filename)
                
        if result[0] == False:
            return redirect("/home")
        else:
            return render_template("register_school.html", user = user, error = True, message = result[1])


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
        matches = 0
        win = 0
        loss = 0
        touch = 0
        position = request.form['position']
        result = create_player(year, first_name, last_name, school, gender, grad_year, player_type, position)
        
        if not request.files.get('file', None):
            pass
        elif result[0] == False:
            file = request.files['file']
            if file and ('.' in file.filename and file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS):
                if not secure_filename(file.filename):
                    return render_template("register_player.html", user = user, error = True, message = "Please upload a secure file.")
                else:
                    filename = str(year) + "_" + str(result[2])  +  "." + file.filename.rsplit(".",1)[1]
                print filename
                file.save(os.path.join("static/player/images", filename))
                add_player_image_names(result[2], year, filename)
                
        if result[0] == False:
            player_id = result[2]
            return redirect("player/"+str(year) + "/"+ str(player_id))
        else:
            return render_template("register_player.html", user = user, error = True, message = result[1])


@app.route("/school/<school_name>")
def show_school_profile(school_name):
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    print "SCHOOL" + school_name
    result = get_school(school_name)
    #### need to get current year
    boys = get_players_by_year_and_school_and_gender(2016, school_name, "Boys Team")
    girls = get_players_by_year_and_school_and_gender(2016, school_name, "Girls Team")
    
    boys_scores = get_gamescores_by_school_and_gender(school_name, "Boys Team")
    girls_scores = get_gamescores_by_school_and_gender(school_name, "Girls Team")

    print school_name
    print "THIS IS THE SCHOOL"
    images = get_school_image(school_name)
    print images
    #images = []
    return render_template("school.html", error = result[0], user = user, data = result[1], boys = boys, boys_scores = boys_scores, girls = girls, girls_scores = girls_scores, images = images) 

@app.route("/edit_school", methods=['GET','POST'])
def edit_school_profile():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if user == 0:
        return redirect("home")
    else:
        result = get_user_school(user)
        if request.method == "GET":
            school = get_school(get_user_school(user))
            girls = school[1][0]
            boys = school[1][1]
            if school[1][0][8] == "Boys Team":
                boys = school[1][0]
                girls = school[1][1]
            return render_template("edit_school.html", user=user, boys = boys, girls = girls)
        else:
            school_name = get_user_school(user)
            street_address = request.form['street_address']
            borough = request.form['borough']
            zipcode = request.form['zipcode']
            girls_teamname = request.form['girls_teamname']
            boys_teamname = request.form['boys_teamname']
            division = request.form['division']
            coach = request.form['coach']
            manager = request.form['manager']
            edit_school(school_name, street_address, borough, zipcode, girls_teamname, boys_teamname, division, coach, manager)
            return redirect("/school/"+result)


@app.route("/player/<year>/<id>")
def show_player_profile(year, id):
    #look up player
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    print "HERE"
    players = get_player(year,id)
    print "\n\n"
    print players
    print "\n\n"
    image = get_player_image(id, year)
    return render_template("player.html", user = user, error = False, players = players, image = image)

@app.route("/user/<username>")
def show_schools(username):
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if user == 0 or user != username:
        return redirect("home")
    else:
        result = get_school(get_user_school(user))
        teams = result[1:][0]
        error = result[0]
        print teams
        
        return render_template("user.html", user = user, teams = teams, error = error)

@app.route("/directory")
def default_directory():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    all_schools = get_distinct_schools()
    return render_template("directory.html", schools = all_schools, user=user)
    #return redirect("directory/")

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "Password"
    create_all_tables()
    app.run(host='0.0.0.0', port=8000)

