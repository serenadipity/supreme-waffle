import sqlite3
import os
from validator import valid_user
import time

from hashlib import sha512
from uuid import uuid4 


###########################

#  INITIAL SETUP

###########################


#####CREATE ALL THE TABLES#########
def create_all_tables():
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()
    
    q = 'CREATE TABLE IF NOT EXISTS users (id INT, username TEXT, password INT, salt INT, school_name TEXT)'
    c.execute(q)
    q = 'CREATE TABLE IF NOT EXISTS schools (school_name TEXT, street_address TEXT, borough TEXT, zipcode TEXT, team TEXT, division TEXT, coach TEXT, manager TEXT, gender TEXT)'
    c.execute(q)
    q = 'CREATE TABLE IF NOT EXISTS events (school_home TEXT, school_away TEXT, date TEXT, time TEXT, game_id INT, status TEXT, address TEXT, gender TEXT)'
    c.execute(q)
    q = 'CREATE TABLE IF NOT EXISTS individual (school_home TEXT, p1id INT, p1touches INT, p1score INT, school_away TEXT, p2id INT, p2touches INT, p2score, date TEXT, gametype TEXT, game_id INT, bout_number INT, address TEXT, year INT, gender TEXT)'
    c.execute(q)
    q = 'CREATE TABLE IF NOT EXISTS info (school TEXT, title TEXT, description TEXT, date TEXT)'
    c.execute(q)
    q = 'CREATE TABLE IF NOT EXISTS images_schools (school_name TEXT, gender TEXT, filename TEXT)'
    c.execute(q)
    q = 'CREATE TABLE IF NOT EXISTS images_players (player_id INT, year INT, filename TEXT)'
    c.execute(q)
    for year in range(20):
        q = 'CREATE TABLE IF NOT EXISTS players_' + str(year + 2000) + ' (year INT, player_id INT, first_name TEXT, last_name TEXT, school TEXT, gender TEXT, grad_year INT, player_type TEXT, position TEXT)'
        c.execute(q)

    conn.close()
    
###########################

#   LOGIN FUNCTIONS

###########################


######## LOGIN ########

def authenticate(username, password):
    #initial connection to database
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor() 

    #finds user database
    q = 'SELECT name FROM sqlite_master WHERE TYPE = "table" AND NAME = "users"'
    c.execute(q)
    if not c.fetchone():
        conn.close()
        return -1

    #checks input w/database
    q = 'SELECT password, salt FROM users WHERE username = ?'
    pepper_and_salt = c.execute(q, (username,)).fetchone()
    if pepper_and_salt and sha512((password + pepper_and_salt[1]) * 10000).hexdigest() == pepper_and_salt[0]:
        q = "SELECT id FROM users WHERE username = ?"
        id = c.execute(q, (username,)).fetchone()
        db.close()
        return id[0]
    db.close()
    return -1

######## REGISTER ########

def register(username, password,repeat_password, school_name):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    #create users table
    q = 'CREATE TABLE IF NOT EXISTS users (id INT, username TEXT, password INT, salt INT, school_name TEXT)'
    c.execute(q)

    #check data is valid
    q = 'SELECT username FROM users'
    users = c.execute(q)
    valid_data = valid_user(username, password, repeat_password, users)
    if not valid_data[0]:
        conn.close()
        return valid_data
    else:
        #hash pw and insert user into table 
        salt = uuid4().hex
        hash_password = sha512((password + salt) * 10000).hexdigest()
        q = 'SELECT COUNT(*) FROM users'
        num_rows = c.execute(q).fetchone()[0]
        q = 'INSERT INTO users (id, username, password, salt, school_name) VALUES (?, ?, ?, ?, ?)'
        print school_name
        c.execute(q, (num_rows + 1, username, hash_password, salt, school_name))
        conn.commit()
        conn.close()
        return [True, "Successful Account Creation"]









###########################

#    IMAGE FUNCTIONS

###########################
    

###### ADD SCHOOL IMAGE NAMES #######
def add_school_image(school_name, gender, filename):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = 'CREATE TABLE IF NOT EXISTS images_schools (school_name TEXT, gender TEXT, filename TEXT)'
    c.execute(q)

    
    q = 'INSERT INTO images_schools (school_name, gender, filename) VALUES (?, ?, ?)'
    print q
    c.execute(q, (school_name, gender, filename))
    conn.commit()
    conn.close()
    return "Success"

###### GET SCHOOL IMAGE NAMES #####
def get_school_image(school_name):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

   
    q = 'SELECT filename FROM images_schools WHERE school_name = ? and gender = "Girls"'
    girls = c.execute(q, (school_name, )).fetchone()
    
    
    images = []
    if girls != None:
        images.append(girls[0])
    else:
        images.append("nope")

    q = 'SELECT filename FROM images_schools WHERE school_name = ? and gender = "Boys"'
    boys = c.execute(q, (school_name, )).fetchone()
    
    if boys != None:
        images.append(boys[0])
    else:
        images.append("nope")

    
    conn.close()
    return images

    
    
###### ADD PLAYER IMAGE NAMES ########
def add_player_image_names(player_id, year, filename):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = 'CREATE TABLE IF NOT EXISTS images_players (player_id INT, year INT, filename TEXT)'
    c.execute(q)

    q = 'INSERT INTO images_players (player_id, year, filename) VALUES (?, ?, ?)'
    c.execute(q, (player_id, year, filename))
    
    conn.commit()
    conn.close()
    return "SUCCESS"

######## GET PLAYER IMAGE #######
def get_player_image(player_id, year):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = 'SELECT filename FROM images_players WHERE player_id = ? and year = ?'
    image = c.execute(q, (player_id, year)).fetchone()
    print image
    conn.close()
    
    if image != None:
        return image[0]
    else:
        return "nope"








    
    

###########################

#     SCHOOL FUNCTIONS

###########################

######## CREATE SCHOOL #########

def create_school(school_name, street_address, borough, zipcode, team, division, coach, manager, gender):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()
    q = 'CREATE TABLE IF NOT EXISTS schools (school_name TEXT, street_address TEXT, borough TEXT, zipcode TEXT, team TEXT, division TEXT, coach TEXT, manager TEXT, gender TEXT)'
    c.execute(q)
    
    #check data is valid
    q = 'SELECT school_name FROM schools WHERE school_name = ? AND gender = ?'
    new  = c.execute(q, (school_name, gender)).fetchone()
    print new
    if not(new is None):
        conn.close()
        return [True, "The " + gender + "' Team from " + school_name + " already exists."]
    else:
        q = 'INSERT INTO schools (school_name, street_address, borough, zipcode, team, division, coach, manager, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        c.execute(q, (school_name, street_address, borough, zipcode, team, division, coach, manager, gender))
        conn.commit()
        conn.close()
        return [False, "Successful School Creation"]

######## GET ALL SCHOOLS ##########
def get_distinct_schools():
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = 'SELECT DISTINCT school_name FROM schools'
    distinct = c.execute(q)
    distinct = [str(x[0]) for x in distinct]
    print distinct
    return distinct

#print get_distinct_schools()

######## GET SCHOOL ########

def get_school(school_name):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    #check data is valid
    q = 'SELECT * FROM schools WHERE school_name = ?'
    new  = c.execute(q, (school_name, )).fetchall()
    if len(new) == 0:
        conn.close()
        return [True, school_name + " is not registered."]
    else:
        conn.commit()
        conn.close()
        return [False, new] 

######## GET USER'S SCHOOl ########
def get_user_school(username):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    #find user's school
    q = """SELECT school_name
           FROM users
           WHERE username = ?"""
    school = c.execute(q, (username, )).fetchone()
    if school == None:
        return ""
    conn.close()
    return school[0]


######## EDIT SCHOOL ########

def edit_school(school_name, street_address, borough, zipcode, girls_teamname, boys_teamname, division, g_coach, g_manager, b_coach, b_manager):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()
    
    #update table
    q = 'UPDATE schools SET street_address = ?, borough = ?, zipcode = ?, division = ?, coach = ?, manager = ?, team = ? WHERE school_name = ? AND gender = "Girls"'
    new  = c.execute(q, (street_address, borough, zipcode, division, g_coach, g_manager, girls_teamname, school_name)).fetchone()
    q = 'UPDATE schools SET street_address = ?, borough = ?, zipcode = ?, division = ?, coach = ?, manager = ?, team = ? WHERE school_name = ? AND gender = "Boys"'
    new  = c.execute(q, (street_address, borough, zipcode, division, b_coach, b_manager, boys_teamname, school_name)).fetchone()
    conn.commit()
    conn.close()
    return new

#edit_school("Stuyvesant High School","345 Chambers Street","Manhattan",10282,"Vipers","",2,"Joel Winston","Max Chan")

######## GET ALL SCHOOL GAMES #########
def get_school_games(school):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    #get array of each game 
    q = "SELECT * from events WHERE school_home = ?"
    home_games = c.execute(q, (school,)).fetchall()
    q = "SELECT * from events where school_away = ?"
    away_games = c.execute(q, (school,)).fetchall()

    return home_games + away_games

######## GET ALL BOUTS ########
def get_all_bouts(school):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()
    return "" 










    
###########################

#     EVENT FUNCTION

###########################

    
######## CREATE EVENT ########

def create_event(school_home, school_away, date, time, game_id, status, address, gender):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    #create events table
    q = 'CREATE TABLE IF NOT EXISTS events (school_home TEXT, school_away TEXT, date TEXT, time TEXT, game_id INT, status TEXT, address TEXT, gender TEXT)'
    c.execute(q)

    #check data is valid
    q = 'SELECT game_id FROM events WHERE game_id = ?'
    new = c.execute(q, (game_id, )).fetchall()
    if len(new) > 0:
        conn.close()
        return [False, "Event already exists"]
    else:
        q = 'INSERT INTO events (school_home, school_away, date, time, game_id, status, address, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        c.execute(q, (school_home, school_away, date, time, game_id, status, address, gender))
        conn.commit()
        conn.close()
        return [True, "Successful Event Creation"]

####### GET ALL EVENTS ########

def get_all_events():
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()
    
    #get all events
    q = 'SELECT * FROM events'
    all_events = c.execute(q).fetchall()
    
    #split future and prev events and sort accordingly
    future_events = [x for x in all_events if str(x[2]) >= time.strftime("%m/%d/%Y")]
    future_events = sorted(future_events, key = lambda event: event[2])
    
    prev_events = [x for x in all_events if str(x[2]) <  time.strftime("%m/%d/%Y")]
    prev_events = sorted(prev_events, key = lambda event: event[2])[::-1]
    
    return [prev_events, future_events]

####### GET EVENT BY GAME ID #######
def get_event_by_id(game_id):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = 'SELECT * FROM events WHERE game_id = ?'
    result = c.execute(q, (game_id, )).fetchone()

    if result == None:
        conn.close()
        return [False, "No such event exists."]
    else:
        conn.commit()
        conn.close()
        return [True, result]

######## UPDATE EVENT ########
def update_event(school_home, school_away, date, time, game_id, status, address, gender):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()
    q = 'UPDATE events SET school_home = ?, school_away = ?, date = ?, time = ?, status = ?, address = ?, gender = ? WHERE game_id = ?'
    new  = c.execute(q, (school_home, school_away, date, time, status, address, gender, game_id)).fetchone()
    conn.commit()
    conn.close()
    return new


    
###########################

#  INDIVIDUAL FUNCTIONS

##########################

######## CREATE INDIVIDUAL SCORELOGS ########

def create_ind(school_home, p1id, p1touches, p1score, school_away, p2id, p2touches, p2score, date, gametype, game_id, bout_number, address, year, gender):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    #create table for individual scores
    q = 'CREATE TABLE IF NOT EXISTS individual (school_home TEXT, p1id INT, p1touches INT, p1score INT, school_away TEXT, p2id INT, p2touches INT, p2score, date TEXT, gametype TEXT, game_id INT, bout_number INT, address TEXT, year INT, gender TEXT)'
    c.execute(q)

    #validation
    q = 'SELECT * FROM individual WHERE school_home = ? AND school_away = ? AND p1id = ? AND p2id = ? AND gender = ? AND game_id = ? AND bout_number = ?'
    new = c.execute(q, (school_home, school_away, p1id, p2id, gender, game_id, bout_number)).fetchone()
    
    if new != None:
        conn.close()
        return [False, "Duplicate bout."]
    
    #adding individual score
    else:
        q = 'INSERT INTO individual (school_home, p1id, p1touches, p1score, school_away, p2id, p2touches, p2score, date, gametype, game_id, bout_number, address, year, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        c.execute(q, (school_home, p1id, p1touches, p1score, school_away, p2id, p2touches, p2score, date, gametype, game_id, bout_number, address, year, gender))
        conn.commit()
        conn.close()
        return [True, "Individual Bout Scores Added."]

#test cases
#print create_ind("Stuyvesant High School", "Kevin Li", 1, 5, "Beacon High School", "Fake Fencer", 2, 3, "5/1/2016", "3pm", "Foil", 2, "345 Chambers St.", "Boys Team")
#create_ind("Stuyvesant High School", "Kevin Li", 1, 5, "Beacon High School", "Other Fake Fencer", 4, 4, "5/1/2016", "3pm", "Foil", 2, "345 Chambers St.", "Boys Team")
#create_ind("Stuyvesant High School", "Kevin Li", 1, 5, "Beacon High School", "Super Fake Fencer", 3, 3, "5/1/2016", "3pm", "Foil", 2, "345 Chambers St.", "Boys Team")
#create_ind("Stuyvesant High School", "Kevin Li", 1, 5, "Beacon High School", "Absolutely Fake Fencer", 7, 2, "5/1/2016", "3pm", "Foil", 2, "345 Chambers St.", "Boys Team")
#create_ind("Stuyvesant High School", "Kevin Li", 1, 5, "Beacon High School", "Very Fake Fencer", 5, 0, "5/1/2016", "3pm", "Foil", 2, "345 Chambers St.", "Boys Team")


######### GET ALL BOUT DATA FOR ONE GAME #########
def get_ind(game_id):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()
    q = "SELECT * FROM individual WHERE game_id = ?"
    results = c.execute(q, (game_id, )).fetchall()
    conn.close()
    for i in results:
        print i[11]
    return results



###########################

#     SCORE CALCULATIONS

###########################


######## GET SCORES PER INDIVIDUAL IN 1 GAME ########
def get_ind_scores(school, player_id, game_id):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    #find number touches made among all bouts
    q = "SELECT p1touches from individual WHERE school_home = ? AND p1_id = ? AND game_id = ?"
    home_scores = c.execute(q, (school, player_id, game_id)).fetchall()
    q = "SELECT p2touches from individual WHERE school_away = ? AND p2_id = ? AND game_id = ?"
    away_scores = c.execute(q, (school, player_id, game_id)).fetchall()
    conn.close()

    #calculate total
    total_score = 0
    scores = home_scores + away_scores
    num_bouts = len(scores)
    for bout in scores:
        total_score += bout[0]
    return [num_bouts, total_score]

#test cases
#print get_ind_scores("Stuyvesant High School", "Kevin Li", 2)
#print "predicted: 25"

######## CALCULATE PLAYER INDICATOR #######
def get_player_indicator(school, player_id, year, gametype):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    #find num touches player made
    q = "SELECT p1touches from individual WHERE school_home = ? AND p1id = ? AND year = ? AND gametype = ?"
    home_scores = c.execute(q, (school, player_id, year, gametype)).fetchall()
    q = "SELECT p2touches from individual WHERE school_away = ? AND p2id = ? AND year = ? AND gametype = ?"
    away_scores = c.execute(q, (school, player_id, year, gametype)).fetchall()

    #sum up player's touches-for
    total_for = 0
    scores_for = home_scores + away_scores
    num_bouts = len(scores_for)
    for bout in scores_for:
        total_for += bout[0]
    
    #find num touches against player
    q = "SELECT p2touches from individual WHERE school_home = ? AND p1id = ? AND year = ? AND gametype = ?"
    away_against = c.execute(q, (school, player_id, year, gametype)).fetchall()
    q = "SELECT p1touches from individual WHERE school_away = ? AND p2id = ? AND year = ? AND gametype = ?"
    home_against = c.execute(q, (school, player_id, year, gametype)).fetchall()

    #sum up player's touches-against
    total_against = 0
    scores_against = home_against + away_against
    num_bouts = len(scores_against)
    for bout in scores_against:
        total_against += bout[0]

    #return final product!
    conn.close()
    return total_for - total_against

#test case
#print get_player_indicator("Stuyvesant High School", "Kevin Li", 2016)
#print "predicted: 13"

######## CALCULATE NO. TOUCHES PLUS WINS AND LOSSES ########
def get_player_touches_and_wins_and_losses(school, player_id, year):
    touches = 0
    wins = 0
    matches = 0
    losses = 0
    
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    #get all instances of player on home 
    q = "SELECT p1touches, p2touches from individual WHERE school_home = ? AND p1id = ? AND year = ?"
    home_touches = c.execute(q, (school, player_id, year)).fetchall()

    #calculate wins and matches
    if home_touches != None:
        matches = len(home_touches)
        wins = sum([1 for bout in home_touches if bout[0] > bout[1]])

    #get all isntances of player on away
    q = "SELECT p1touches, p2touches from individual WHERE school_away = ? AND p2id = ? AND year = ?"
    away_touches = c.execute(q, (school, player_id, year)).fetchall()

    #calculate wins and matches
    if away_touches != None:
        matches += len(away_touches)
        wins += sum([1 for bout in home_touches if bout[1] > bout[0]])

    #calculate losses
    losses = matches - wins

    #calculate total touches made by player
    for bout in home_touches:
        touches += bout[0]
    for bout in away_touches:
        touches += bout[1]

    return [matches, touches, wins, losses]

#print get_player_touches("Stuyvesant High School", "Kevin Li", 2016)
#print "expected: idk like 25???"

####### GET ALL TEAM INDICATORS ##########
def get_all_team_indicators():
    all_schools = get_distinct_schools()
    epee_girls = []
    foil_girls = []
    epee_boys = []
    foil_boys = []
    all_girls = []
    all_boys = []
    for school in all_schools:
        epee_girls.append([school, sum(get_team_indicators(time.strftime("%Y"), school, "Girls", "Epee")[0])])
        foil_girls.append([school, sum(get_team_indicators(time.strftime("%Y"), school, "Girls", "Foil")[0])])
        epee_boys.append([school, sum(get_team_indicators(time.strftime("%Y"), school, "Boys", "Epee")[0])])
        foil_boys.append([school, sum(get_team_indicators(time.strftime("%Y"), school, "Boys", "Foil")[0])])

    for i in range(len(epee_girls)):
        all_girls.append([epee_girls[i][0], epee_girls[i][1] + foil_girls[i][1]])

    for i in range(len(epee_boys)):
        all_boys.append([epee_boys[i][0], epee_boys[i][1] + foil_boys[i][1]])

    epee_girls.sort(key = lambda student : student[1])
    foil_girls.sort(key = lambda student : student[1])
    epee_boys.sort(key = lambda student : student[1])
    foil_boys.sort(key = lambda student : student[1])
    all_girls.sort(key = lambda student : student[1])
    all_boys.sort(key = lambda student : student[1])

    return [epee_girls[::-1], foil_girls[::-1], epee_boys[::-1], foil_boys[::-1], all_girls[::-1], all_boys[::-1]]


####### get specific team indicator ########
def get_team_indicators(year, school, gender, gametype):
    #set up connection YET AGAIN
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    names = []
    indicator_list = []
    combined = []
    q = """SELECT first_name, last_name, player_id 
           FROM players_""" + str(year) + """ 
           WHERE school = ? AND player_type = ? AND gender = ?"""
    #print q
    playerlist = c.execute(q, (school, gametype, gender)).fetchall()
    #print playerlist
    #print "\n\n\n PLAYER LIST \n\n\n"
    #loop de loop through players
    for players in playerlist:
        name = players[0] + " " + players[1]
        ind = get_player_indicator(school, players[2], year, gametype)
        names.append(name)
        indicator_list.append(ind)
        combined.append([school, name, ind])

    combined.sort(key = lambda student : student[2])
    #print indicator_list
    #print "\n\n\n INDICATOR LIST \n\n\n"
    #print combined
    #print "\n\n\n combined \n\n\n"
    return [indicator_list, names, combined]
#print get_player_indicator("Kevin Li", 1, 2016, "Epee")
#print get_team_indicators(2016, "Stuyvesant High School", "Boys Team", "Epee")

##### get total team indicator ########
def get_total_team_indicator(year, school, gender, gametype):
    indicatorlist = get_team_indicators(year, school, gender, gametype)[0]
    return sum(indicatorlist)

### even more functions ##
def get_gender_indicator(year, school, gender):
    return get_total_team_indicator(year, school, gender, "Foil") + get_total_team_indicator(year, school, gender, "Epee")

######Get Player Indicators #########
def get_all_player_indicators():
    all_schools = get_distinct_schools()
    epee_girls = []
    foil_girls = []
    epee_boys = []
    foil_boys = []
    all_girls = []
    all_boys = []
    for school in all_schools:
        epee_girls += get_team_indicators(time.strftime("%Y"), school, "Girls", "Epee")[2]
        foil_girls += get_team_indicators(time.strftime("%Y"), school, "Girls", "Foil")[2]
        epee_boys += get_team_indicators(time.strftime("%Y"), school, "Boys", "Epee")[2]
        foil_boys += get_team_indicators(time.strftime("%Y"), school, "Boys", "Foil")[2]

    
    epee_girls.sort(key = lambda student : student[2])
    foil_girls.sort(key = lambda student : student[2])
    epee_boys.sort(key = lambda student : student[2])
    foil_boys.sort(key = lambda student : student[2])

    return [epee_girls[::-1], foil_girls[::-1], epee_boys[::-1], foil_boys[::-1]]

######## GET PLAYER BY YEAR, SCHOOL, TYPE, GENDER #######
def get_team_players(year, school, gametype, gender):
    #set up connection..... again.....
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = "SELECT * FROM players_" + str(year) + " WHERE school = ? AND player_type = ? AND gender = ?"
    players = c.execute(q, (school, gametype, gender)).fetchall()

    return players

#get_team_players(2016, "Stuyvesant High School", "Epee", "Boys Team")



######## GET GAMESCORES BY SCHOOL ########
"""def get_gamescores_by_school_and_gender(school, gender):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = "SELECT home_score from events WHERE school_home = ? AND gender = ?"
    home_scores = c.execute(q, (school, gender)).fetchall()
    q = "SELECT away_score from events WHERE school_away = ? AND gender = ?"
    away_scores = c.execute(q, (school, gender)).fetchall()
    conn.close()

    total_score = 0;
    scores = home_scores + away_scores
    num_games = len(scores)
    for game in scores:
        total_score += game[0]
    return [num_games, total_score]"""

#create_event("Stuyvesant High School", 20, "Bronx Science", 15, "02/15/2016", "4:00pm", 22745, "", "345 Chambers Street","Girls Team")
#create_event("Brooklyn Tech", 35, "Stuyvesant High School", 20, "04/25/2016", "5:30pm", 36375, "", "345 Chambers Street","Girls Team")

#create_event("Stuyvesant High School", 20, "Bronx Science", 30, "01/15/2016", "4:00pm", 22365, "", "345 Chambers Street","Boys Team")
#create_event("Brooklyn Tech", 35, "Stuyvesant High School", 40, "03/25/2016", "5:30pm", 35325, "", "345 Chambers Street","Boys Team")

#print get_gamescores_by_school_and_gender("Stuyvesant High School","Girls Team")
#print get_gamescores_by_school_and_gender("Stuyvesant High School","Boys Team")









###########################

#     PLAYER FUNCTIONS

###########################


######## CREATE PLAYER ########

def create_player(year, first_name, last_name, school, gender, grad_year, player_type, position, check):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    #create players table
    q = 'CREATE TABLE IF NOT EXISTS players_' + str(year) + ' (year INT, player_id INT, first_name TEXT, last_name TEXT, school TEXT, gender TEXT, grad_year INT, player_type TEXT, position TEXT)'
    c.execute(q)

    q = 'CREATE TABLE IF NOT EXISTS years (year INT)'
    c.execute(q)

    q = 'SELECT year FROM years'
    all_years = c.execute(q).fetchall()

    if (year not in all_years):
        q = 'INSERT INTO years (year) VALUES (?)'
        c.execute(q, (year, ))

    q = 'SELECT COUNT(*) FROM players_' + str(year) 
    num_players = c.execute(q).fetchone()[0]
    
    #checks that player exists
    q = 'SELECT * FROM players_' + str(year) + ' WHERE first_name = ? AND last_name = ? AND school = ?'
    new = c.execute(q, (first_name, last_name, school)).fetchone()
    if new != None: 
        #confirms same name isnt a mistake
        #this doesn't help the user confirm since it's a terminal thing
        #i know it's just a placeholder! 
        #if(confirm(prompt="Player of the same name already exists at this school. Proceed anyways?")):
        if (check == True):
            q = 'INSERT INTO players_' + str(year) + ' (year, player_id, first_name, last_name, school, gender, grad_year, player_type, position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
            c.execute(q, (year, num_players + 1, first_name, last_name, school, gender, grad_year, player_type, position))
            conn.commit()
            conn.close()
            return [False, "Successful Player Creation", num_players + 1]
        else: 
            return [True, "Player with same name and school are already exists. Submit again to create anyway."]
    #add player
    q = 'INSERT INTO players_' + str(year) + ' (year, player_id, first_name, last_name, school, gender, grad_year, player_type, position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    c.execute(q, (year, num_players + 1, first_name, last_name, school, gender, grad_year, player_type, position))
    conn.commit()
    conn.close()
    return [False, "Successful Player Creation", num_players + 1]

######## GET PLAYER BY YEAR, SCHOOL, TYPE, GENDER #######
def get_team_players(year, school, gametype, gender):
    #set up connection..... again.....
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = "SELECT * FROM players_" + str(year) + " WHERE school = ? AND player_type = ? AND gender = ?"
    players = c.execute(q, (school, gametype, gender)).fetchall()

    return players

######## GET PLAYER ########
def get_player(year, id):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = """SELECT * 
           FROM players_""" + str(year) + """
           WHERE player_id = ?"""
    player = c.execute(q, (id,)).fetchone()
    conn.close()
    stringified = []
    for item in player:
        stringified.append(str(item))
    return stringified
           

######## GET PLAYERS BY YEAR ########
def get_players_by_year_and_gender(year, gender):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = """SELECT * 
           from players_""" + str(year) + """
           WHERE gender = ?"""
    players = c.execute(q, (gender,)).fetchone()
    conn.close()
    return players


#print get_player(2014,1)
#print get_players_by_year_and_gender(2014, "Girls Team")


######## GET ALL PLAYERS BY YEAR AND GENDER ########
def get_all_players_by_year_and_gender(year, gender):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = """SELECT * 
           from players_""" + str(year) + """
           WHERE gender = ?"""
    players = c.execute(q, (gender,)).fetchall()
    conn.close()
    return players



######## GET PLAYERS BY YEAR, SCHOOL, and GENDER ########
def get_players_by_year_and_school_and_gender(year, school, gender):
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()

    q = """SELECT * 
           from players_""" + str(year) + """
           WHERE school = ? AND gender = ?"""
    players = c.execute(q, (school, gender)).fetchall()
    conn.close()
    return players

# print get_players_by_year_and_school(2016, "Stuyvesant High School", "Girls")


######## EDIT PLAYER ########

def edit_player(year, id, first_name, last_name, school, gender, grad_year, player_type, position):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")
    c = conn.cursor()
    
    #update table
    q = 'UPDATE players_' + str(year) + ' SET first_name = ?, last_name = ?, gender = ?, grad_year = ?, player_type = ?, position = ? WHERE school = ? AND player_id = ?'
    new  = c.execute(q, (first_name, last_name, gender, grad_year, player_type, position, school, id)).fetchone()
    conn.commit()
    conn.close()
    return new






###########################

#     INFO FUNCTIONS

###########################


######## ADD ADDITIONAL INFO ########

def create_info(school, title, description, date):
    #set up connection
    conn = sqlite3.connect(os.path.dirname("data.db") + "data.db")   
    c = conn.cursor()

    #create info table
    q = 'CREATE TABLE IF NOT EXISTS info (school TEXT, title TEXT, description TEXT, date TEXT)'
    c.execute(q)

    #add info
    q = 'INSERT INTO info (school, title, description, date) VALUES (?, ?)'
    c.execute(q, (school, title, description, date))
    conn.commit()
    conn.close()
    return [True, "Successful Info Creation"]
