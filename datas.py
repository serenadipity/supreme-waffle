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

def create_event(school_home, home_score, school_away, away_score, date, time, game_id, status, address, gender):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #create events table
    q = 'CREATE TABLE IF NOT EXISTS events (school_home TEXT, home_score INT, school_away TEXT, away_score INT, date TEXT, time TEXT, game_id INT, status TEXT, address TEXT, gender TEXT)'
    c.execute(q)

    #check data is valid
    q = 'SELECT game_id FROM events WHERE game_id = ?'
    new = c.execute(q, (game_id, )).fetchall()
    if len(new) > 0:
        conn.close()
        return [False, "Event already exists"]
    else:
        q = 'INSERT INTO events (school_home, home_score, school_away, away_score, date, time, game_id, status, address, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        c.execute(q, (school_home, home_score, school_away, away_score, date, time, game_id, status, address, gender))
        conn.commit()
        conn.close()
        return [True, "Successful Event Creation"]

######## CREATE INDIVIDUAL SCORELOGS ########

def create_ind(school_home, player1, p1id, p1touches, school_away, player2, p2id, p2touches, date, time, gametype, game_id, address):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #create table for individual scores
    q = 'CREATE TABLE IF NOT EXISTS individual (school_home TEXT, player1 TEXT, p1id INT, p1touches INT, school_away TEXT, player2 TEXT, p2id INT, p2touches INT, date TEXT, time TEXT, gametype TEXT, game_id INT, address TEXT)'
    c.execute(q)

    #validation
    q = 'SELECT * FROM individual WHERE school_home = ? AND school_away = ? AND p1id = ? AND p2id = ?'
    new = c.execute(q, (school_home, school_away, p1id, p2id)).fetchone()
    if new != None:
        conn.close()
        return [False, "Duplicate bout."]

    #adding individual score
    else:
        q = 'INSERT INTO individual (school_home, player1, p1id, p1touches, school_away, player2, p2id, p2touches, date, time, gametype, game_id, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        c.execute(q, (school_home, player1, p1id, p1touches, school_away, player2, p2id, p2touches, date, time, gametype, game_id, address))
        conn.commit()
        conn.close()
        return [True, "Individual Bout Scores Added."]

######## GET SCORES PER INDIVIDUAL IN 1 GAME ########
def get_ind_scores(school, player, game_id):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #find number touches made among all bouts
    q = "SELECT p1touches from individual WHERE school_home = ? AND player1 = ? AND game_id = ?"
    home_scores = c.execute(q, (school, player, game_id)).fetchall()
    q = "SELECT p2touches from individual WHERE school_away = ? AND player2 = ? AND game_id = ?"
    away_scores = c.execute(q, (school, player, game_id)).fetchall()
    conn.close()

    #calculate total
    total_score = 0
    scores = home_scores + away_scores
    num_bouts = len(scores)
    for bout in scores:
        total_score += bout[0]
    return [num_bouts, total_score]

######## CALCULATE INDICATOR #######
def get_indicator(school, player):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #find num touches player made
    q = "SELECT p1touches from individual WHERE school_home = ? AND player1 = ?"
    home_scores = c.execute(q, (school, player)).fetchall()
    q = "SELECT p2touches from individual WHERE school_away = ? AND player2 = ?"
    away_scores = c.execute(q, (school, player)).fetchall()

    #sum up player's touches-for
    total_for = 0
    scores_for = home_scores + away_scores
    num_bouts = len(scores_for)
    for bout in scores_for:
        total_for += bout[0]
    
    #find num touches against player
    q = "SELECT p2touches from individual WHERE school_home = ? AND player1 = ?"
    away_against = c.execute(q, (school, player)).fetchall()
    q = "SELECT p1touches from individual WHERE school_away = ? AND player2 = ?"
    home_against = c.execute(q, (school, player)).fetchall()

    #sum up player's touches-against
    total_against = 0
    scores_against = home_against + away_against
    num_bouts = len(scores_against)
    for bout in scores_against:
        total_against += bout[0]

    #return final product!
    conn.close()
    return total_for - total_against

    
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
        #i know it's just a placeholder! 
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


######## GET PLAYERS BY YEAR, SCHOOL, and GENDER ########
def get_players_by_year_and_school_and_gender(year, school, gender):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    q = """SELECT * 
           from players_""" + str(year) + """
           WHERE school = ? AND gender = ?"""
    players = c.execute(q, (school, gender)).fetchall()
    conn.close()
    return players

# print get_players_by_year_and_school(2016, "Stuyvesant High School", "Girls Team")


######## GET GAMESCORES BY SCHOOL ########
def get_gamescores_by_school_and_gender(school, gender):
    conn = sqlite3.connect("data.db")
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
    return [num_games, total_score]

#create_event("Stuyvesant High School", 20, "Bronx Science", 15, "02/15/2016", "4:00pm", 22745, "", "345 Chambers Street","Girls Team")
#create_event("Brooklyn Tech", 35, "Stuyvesant High School", 20, "04/25/2016", "5:30pm", 36375, "", "345 Chambers Street","Girls Team")

#create_event("Stuyvesant High School", 20, "Bronx Science", 30, "01/15/2016", "4:00pm", 22365, "", "345 Chambers Street","Boys Team")
#create_event("Brooklyn Tech", 35, "Stuyvesant High School", 40, "03/25/2016", "5:30pm", 35325, "", "345 Chambers Street","Boys Team")

#print get_gamescores_by_school_and_gender("Stuyvesant High School","Girls Team")
#print get_gamescores_by_school_and_gender("Stuyvesant High School","Boys Team")



######## EDIT SCHOOL ########

def edit_school(school_name, street_address, borough, zipcode, girls_teamname, boys_teamname, division, coach, manager):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    
    #update table
    q = 'UPDATE schools SET street_address = ?, borough = ?, zipcode = ?, division = ?, coach = ?, manager = ?, team = ? WHERE school_name = ? AND gender = "Girls Team"'
    new  = c.execute(q, (street_address, borough, zipcode, division, coach, manager, girls_teamname, school_name)).fetchone()
    q = 'UPDATE schools SET street_address = ?, borough = ?, zipcode = ?, division = ?, coach = ?, manager = ?, team = ? WHERE school_name = ? AND gender = "Boys Team"'
    new  = c.execute(q, (street_address, borough, zipcode, division, coach, manager, boys_teamname, school_name)).fetchone()
    conn.commit()
    conn.close()
    return 

edit_school("Stuyvesant High School","345 Chambers Street","Manhattan",10282,"Vipers","",2,"Joel Winston","Max Chan")
#create_school("Stuyvesant High School","345 Chambers St","Manhattan",10282,"Vipers",2,"Joel Winston","Max Chan","Girls Team")
