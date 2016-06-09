from flask import Flask, render_template, request, session, redirect, url_for
import os, json
from werkzeug import secure_filename
import datetime
now = datetime.datetime.now()
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
    all_events = get_all_events()
    prev_events = all_events[0]
    future_events = all_events[1]

    print prev_events
    print future_events
    return render_template("home.html", user = user, prev_events = prev_events, future_events = future_events)


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
        return render_template("register_player.html", user=user, error = False)
    else:
        year = request.form['year']
        first_name = request.form['fname']
        last_name = request.form['lname']
        school = get_user_school(user)
        gender = request.form['gender']
        grad_year = request.form['grad_year']
        player_type = request.form['player_type']
        position = request.form['position']
        check = request.form['check']
        if check == "Register Again":
            check = True
        else:
            check = False
        result = create_player(year, first_name, last_name, school, gender, grad_year, player_type, position, check)

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
            message = result[1]
            return render_template("register_player.html", user = user, error = True, message = result[1], year = year, first_name = first_name, last_name = last_name, school = school, gender = gender, grad_year = grad_year, player_type = player_type, position = position)


@app.route("/school/<school_name>")
def show_school_profile(school_name):
    if 'user' not in session:
        session['user'] = 0
    if session['user'] != 0:
        user_school = get_user_school(session['user'])
    else:
        user_school = ""
    user = session['user']

    result = get_school(school_name)
   
    boys = get_players_by_year_and_school_and_gender(now.year, school_name, "Boys")
    girls = get_players_by_year_and_school_and_gender(now.year, school_name, "Girls")

    images = get_school_image(school_name)

    return render_template("school.html", error = result[0], user = user, school_name = school_name, user_school = user_school, data = result[1:], boys = boys, girls = girls, images = images)

@app.route("/graph")
def graph():
    school = request.args.get("school").replace("&#39;","'")
    graph = []
    graph.append(get_team_indicators(now.year, school, "Girls", "Epee")[2])
    graph.append(get_team_indicators(now.year, school, "Girls", "Foil")[2])
    graph.append(get_team_indicators(now.year, school, "Boys", "Epee")[2])
    graph.append(get_team_indicators(now.year, school, "Boys", "Foil")[2])
    return json.dumps(graph)

@app.route("/edit_school", methods=['GET','POST'])
def edit_school_profile():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if user == 0:
        return redirect("login")
    else:
        result = get_user_school(user)
        if request.method == "GET":
            user_school = get_user_school(user)
            school = get_school(user_school)
            girls = ['','','','','','','','','']
            boys = ['','','','','','','','','']
            if len(school) > 2:
                if school[1][0][8] == "Girls":
                    girls = school[1][0]
                    boys = school[1][1]
                else:
                    boys = school[1][0]
                    girls = school[1][1]
            else:
                if school[1][0][8] == "Girls":
                    girls = school[1][0]
                else:
                    boys = school[1][0]
            if len(school) > 1:
                school = school[1][0]
            else:
                school = ['','','','','','','','','']
            return render_template("edit_school.html", user=user, user_school = user_school, boys = boys, girls = girls, school = school)
        else:
            school_name = get_user_school(user)
            street_address = request.form['street_address']
            borough = request.form['borough']
            zipcode = request.form['zipcode']
            girls_teamname = request.form['girls_teamname']
            boys_teamname = request.form['boys_teamname']
            division = request.form['division']
            g_coach = request.form['g_coach']
            g_manager = request.form['g_manager']
            b_coach = request.form['b_coach']
            b_manager = request.form['b_manager']
            edit_school(school_name, street_address, borough, zipcode, girls_teamname, boys_teamname, division, g_coach, g_manager, b_coach, b_manager)
            return redirect("/school/"+result)


@app.route("/player/<year>/<id>")
def show_player_profile(year, id):
    #look up player
    if 'user' not in session:
        session['user'] = 0
    if session['user'] != 0:
        user_school = get_user_school(session['user'])
    else:
        user_school = ""
    user = session['user']
    player = get_player(year,id)
    image = get_player_image(id, year)
    indicator = get_player_indicator(player[4], id, year, player[7])
    touches_info = get_player_touches_and_wins_and_losses(player[4], id, year)
    return render_template("player.html", user = user, user_school = user_school, error = False, player = player, image = image, indicator = indicator, touches_info = touches_info)

@app.route("/edit_player/<year>/<id>", methods=['GET','POST'])
def edit_player_profile(year,id):
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if user == 0:
        return redirect("login")
    else:
        player = get_player(year, id)
        user_school = get_user_school(user)
        if request.method == "GET":
            error = False
            message = ''
            if player[4] != user_school:
                error = True
                message = "You can only edit profiles for your school's players."
            return render_template("edit_player.html", user=user, error=error, message=message, player=player)
        else:
            first_name = request.form['fname']
            last_name = request.form['lname']
            school = get_user_school(user)
            gender = request.form['gender']
            grad_year = request.form['grad_year']
            player_type = request.form['player_type']
            position = request.form['position']
            edit_player(year, id, first_name, last_name, school, gender, grad_year, player_type, position)
            return redirect("/player/"+year+"/"+id)

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

@app.route("/input_stats/<username>", methods=['GET','POST'])
def input_stats(username):
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if user == 0 or user != username:
        return redirect("login")
    else:
        schools = get_distinct_schools()
        user_school = get_user_school(username)
        if request.method == "GET":
            return render_template("input_stats.html",user_school=user_school,schools=schools, user = user)
        else:
            current_page = request.form['input_page_num']
            if current_page == "1":
                school_home = request.form['school_home']
                school_away = request.form['school_away']
                weapon = request.form['weapon']
                gender = request.form['gender']
                game_id = request.form['game_id']
                date = request.form['date']
                address = request.form['location']
                error = False
                if school_home == school_away:
                    error = True
                    message = "Home School and Away School cannot be the same."
                if school_home != user_school and school_away != user_school:
                    error = True
                    message = "You can only input data for events your school participated in."
                if error == True:
                    return render_template("input_stats.html",error=error,message=message,schools=schools)
                else:
                    home_players = get_players_by_year_and_school_and_gender(now.year,school_home,gender)
                    away_players = get_players_by_year_and_school_and_gender(now.year,school_away,gender)
                    return render_template("input_stats2.html",school_home=school_home,school_away=school_away,home_players=home_players,away_players=away_players,gender=gender,weapon=weapon,game_id=game_id,address=address)
            elif current_page == "2":
                home_starter1 = request.form['home_starter1']
                home_starter1 = get_player(now.year,home_starter1)
                home_starter2 = request.form['home_starter2']
                home_starter2 = get_player(now.year,home_starter2)
                home_starter3 = request.form['home_starter3']
                home_starter3 = get_player(now.year,home_starter3)
                away_starter1 = request.form['away_starter1']
                away_starter1 = get_player(now.year,away_starter1)
                away_starter2 = request.form['away_starter2']
                away_starter2 = get_player(now.year,away_starter2)
                away_starter3 = request.form['away_starter3']
                away_starter3 = get_player(now.year,away_starter3)
                school_home = request.form['school_home']
                school_away = request.form['school_away']
                weapon = request.form['weapon']
                gender = request.form['gender']
                game_id = request.form['game_id']
                date = request.form['date']
                address = request.form['address']

                home_players = get_players_by_year_and_school_and_gender(now.year,school_home,gender)
                away_players = get_players_by_year_and_school_and_gender(now.year,school_away,gender)

                return render_template("input_stats3.html",home_starter1=home_starter1,home_starter2=home_starter2,home_starter3=home_starter3,away_starter1=away_starter1,away_starter2=away_starter2,away_starter3=away_starter3,school_home=school_home,school_away=school_away,gender=gender,weapon=weapon,date=date,address=address,game_id=game_id,home_players=home_players,away_players=away_players)
            elif current_page == "3":
                school_home = request.form['school_home']
                school_away = request.form['school_away']
                gametype = request.form['weapon']
                gender = request.form['gender']
                game_id = request.form['game_id']
                date = request.form['date']
                address = request.form['address']
                year = now.year

                for i in range(1,9):
                    p1 = request.form['b'+str(i)+'_home']
                    p2 = request.form['b'+str(i)+'_away']
                    create_ind(school_home, p1, request.form['b'+str(i)+'_home_touches'], request.form['b'+str(i)+'_home_score'], school_away, p2, request.form['b'+str(i)+'_away_touches'], request.form['b'+str(i)+'_away_score'], date, gametype, game_id, 1, address, year, gender)

                user_school = get_user_school(username)
                return redirect("school/"+user_school)

@app.route("/event/<game_id>")
def event(game_id):
    if 'user' not in session:
        session['user'] = "0"
    user = session['user']
    user_school = get_user_school(user)
    data = get_ind(game_id)
    result = get_event_by_id(game_id)
    event = result[1]
    year = result[1][2][6:10]
    players = []
    for i in data:
        player1 = get_player(year,i[1])
        player2 = get_player(year,i[5])
        players.append(player1[2]+' '+player1[3])
        players.append(player2[2]+' '+player2[3])
    return render_template("event.html", user = user, user_school = user_school, data=data, game=event, players=players)


@app.route("/register_event", methods=['GET','POST'])
def register_event():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if user == 0:
        return redirect("login")
    else:
        if request.method=="GET":
            schools = get_distinct_schools()
            return render_template("register_event.html",user=user,schools=schools)
        else:
            school_home=request.form['school_home']
            school_away=request.form['school_away']
            date=request.form['date']
            time=request.form['time']
            game_id=request.form['game_id']
            status=request.form['status']
            address=request.form['address']
            gender=request.form['gender']
            result=create_event(school_home,school_away,date,time,game_id,status,address,gender)
            return render_template("register_event.html",user=user,error=True,message=result[1])

@app.route("/edit_event/<game_id>", methods=['GET','POST'])
def edit_event(game_id):
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    if user == 0:
        return redirect("login")
    else:
        if request.method=="GET":
            school = get_user_school(user)
            result = get_event_by_id(game_id)
            event = result[1]
            schools = get_distinct_schools()
            error = False
            message = ""
            if result[0] == False:
                error = True
                message = "This event does not exist."
            else:
                if event[0] != school and event[1] != school:
                    error = True
                    message = "You can only edit events for your own school."
            return render_template("edit_event.html",user=user,error=error,message=message,game=event,schools=schools)
        else:
            school_home=request.form['school_home']
            school_away=request.form['school_away']
            date=request.form['date']
            time=request.form['time']
            game_id=request.form['game_id']
            status=request.form['status']
            address=request.form['address']
            gender=request.form['gender']
            result=update_event(school_home,school_away,date,time,game_id,status,address,gender)
            return render_template("edit_event.html",user=user,error=True,message="Event updated.")


@app.route("/directory")
def default_directory():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']
    all_schools = sorted(get_distinct_schools(), key = lambda item : item)
    return render_template("directory.html", schools = all_schools, user=user)

@app.route("/roster")
def current_roster():
    school = request.args.get("school")
    boys = get_players_by_year_and_school_and_gender(2016, school, "Boys")
    girls = get_players_by_year_and_school_and_gender(2016, school, "Girls")
    roster = {'boys': boys, 'girls': girls}
    return json.dumps(roster)

@app.route("/rankings")
def rankings():
    if 'user' not in session:
        session['user'] = 0
    user = session['user']

    school_indicators = get_all_team_indicators()
    ges = school_indicators[0]
    gfs = school_indicators[1]
    bes = school_indicators[2]
    bfs = school_indicators[3]
    gos = school_indicators[4]
    bos = school_indicators[5]
    
    player_indicators = get_all_player_indicators()
    gep = player_indicators[0]
    gfp = player_indicators[1]
    bep = player_indicators[2]
    bfp = player_indicators[3]
    
    return render_template("rankings.html", user = user, ges = ges, gfs = gfs, bes = bes, bfs = bfs, gos = gos, bos = bos, gep = gep, gfp = gfp, bep = bep, bfp = bfp)

app.secret_key = "woohoo softdev"
create_all_tables()

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "Password"
    create_all_tables()
    app.run(host='0.0.0.0', port=8000)
