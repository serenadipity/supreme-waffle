import sqlite3
from validator import valid_user
from confirmtest import confirm

from hashlib import sha512
from uuid import uuid4 


######## LOGIN ########

def authenticate(username, password):
    #initial connection to database
    db = sqlite3.connect("data.db")
    c = db.cursor() 

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
    conn = sqlite3.connect("data.db")
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
        c.execute(q, (num_rows + 1, username, hash_password, salt, school_name))
        conn.commit()
        conn.close()
        return [True, "Successful Account Creation"]

######## CREATE SCHOOL ########

def create_school(school_name, street_address, borough, zipcode, team, division, coach, manager, gender):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    print "SCHOOL NAME" + school_name
    #create users table
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


######## CREATE EVENT ########

def create_event(school_home, home_score, school_away, away_score, date, time, game_id, status, address):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #create events table
    q = 'CREATE TABLE IF NOT EXISTS events (school_home TEXT, home_score INT, school_away TEXT, away_score INT, date TEXT, time TEXT, game_id INT, status TEXT, address TEXT)'
    c.execute(q)

    #check data is valid
    q = 'SELECT game_id FROM events WHERE game_id = ?'
    new = c.execute(q, (game_id, )).fetchall()
    if len(new) > 0:
        conn.close()
        return [False, "Event already exists"]
    else:
        q = 'INSERT INTO events (school_home, home_score, school_away, away_score, date, time, game_id, status, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        c.execute(q, (school_home, home_score, school_away, away_score, date, time, game_id, status, address))
        conn.commit()
        conn.close()
        return [True, "Successful Event Creation"]

######## CREATE PLAYER ########

def create_player(year, first_name, last_name, school, gender, grad_year, player_type, matches, win, loss, touch, position):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #create players table
    q = 'CREATE TABLE IF NOT EXISTS players_' + str(year) + ' (year INT, player_id INT, first_name TEXT, last_name TEXT, school TEXT, gender TEXT, grad_year INT, player_type TEXT, matches INT, win INT, loss INT, touch INT, position TEXT)'
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
        if(confirm(prompt="Player of the same name already exists at this school. Proceed anyways?")): 
            q = 'INSERT INTO players_' + str(year) + ' (year, player_id, first_name, last_name, school, gender, grad_year, player_type, matches, win, loss, touch, position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  ?)'
            c.execute(q, (year, num_players + 1, first_name, last_name, school, gender, grad_year, player_type, matches, win, loss, touch, position))
            conn.commit()
            conn.close()
            return [False, "Successful Player Creation", num_players + 1]
        else: 
            return [True, "Player not created"]
    #add player
    q = 'INSERT INTO players_' + str(year) + ' (year, player_id, first_name, last_name, school, gender, grad_year, player_type, matches, win, loss, touch, position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    c.execute(q, (year, num_players + 1, first_name, last_name, school, gender, grad_year, player_type, matches, win, loss, touch, position))
    conn.commit()
    conn.close()
    return [False, "Successful Player Creation", num_players + 1]

######## ADD ADDITIONAL INFO ########

def create_info(school, title, description, date):
    #set up connection
    conn = sqlite3.connect("data.db")
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

######## GET ALL SCHOOLS ##########
def get_distinct_schools():
    conn = sqlite3.connect("data.db")
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
    conn = sqlite3.connect("data.db")
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
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #find user's school
    q = """SELECT school_name 
           FROM users
           WHERE username = ?"""
    school = c.execute(q, (username, )).fetchone()
    conn.close()
    return school[0]

######## GET PLAYER ########
def get_player(year, id):
    conn = sqlite3.connect("data.db")
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
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    q = """SELECT * 
           from players_""" + str(year) + """
           WHERE gender = ?"""
    players = c.execute(q, (gender,)).fetchone()
    conn.close()
    return players


#print get_player(2014,1)
#print get_players_by_year_and_gender(2014, "Girls Team")


######## GET PLAYERS BY YEAR AND SCHOOL ########
def get_players_by_year_and_school(year, school):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    q = """SELECT * 
           from players_""" + str(year) + """
           WHERE school = ?"""
    players = c.execute(q, (school,)).fetchall()
    conn.close()
    return players

#print get_players_by_year_and_school(2016, "Stuyvesant High School")


######## GET GAMESCORES BY SCHOOL ########
def get_gamescores_by_school(school):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    q = "SELECT home_score from events WHERE school_home = ?"
    home_scores = c.execute(q, (school,)).fetchall()
    q = "SELECT away_score from events WHERE school_away = ?"
    away_scores = c.execute(q, (school,)).fetchall()
    conn.close()

    total_score = 0;
    scores = home_scores + away_scores
    num_games = len(scores)
    for game in scores:
        total_score += game[0]
    return [num_games, total_score]

create_event("Stuyvesant High School", 20, "Bronx Science", 15, "02/15/2016", "4:00pm", 22745, "", "345 Chambers Street")

create_event("Brooklyn Tech", 35, "Stuyvesant High School", 20, "04/25/2016", "5:30pm", 36375, "", "345 Chambers Street")

print get_gamescores_by_school("Stuyvesant High School")

