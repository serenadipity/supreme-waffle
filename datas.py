import sqlite3 
import utils

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
    if not c.fetchone()
        conn.close()
        return -1

    #checks input w/database
    q = 'SELECT password, salt FROM users WHERE username = ?'
    pepper_and_salt = c.execute(q, (username,)).fetchone()
    if pepper_and_salt and sha512((password + pepper_and_salt[1]) * 10000).hexdigest() == pepper_and_salt[0]:
        q = "SELECT id FROM users WHERE username = ?"
        id = c.execute(q, (username,)).fetchone()
        conn.close()
        return id[0]
    conn.close()
    return -1

######## REGISTER ########

def register(username, password, school_name):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #create users table
    q = 'CREATE TABLE IF NOT EXISTS users (id INT, username TEXT, password INT, salt INT, school_name TEXT)'
    c.execute(q)

    #check data is valid
    q = 'SELECT username FROM users'
    users = c.execute(q)
    valid_data = validator.valid_user(username, password, repeat_password, users)
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
        c.execute(q, (num_rows + 1, username, hash_password, salt, first_name, last_name, email))
        conn.commit()
        conn.close()
        return [True, "Successful Account Creation"]

######## CREATE SCHOOL ########

def create_school(school_name, street_address, borough, zipcode, team, division, coach, manager, gender):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #create users table
    q = 'CREATE TABLE IF NOT EXISTS schools (school_name TEXT, street_address TEXT, borough TEXT, zipcode TEXT, team TEXT, division TEXT, coach TEXT, manager TEXT, gender TEXT)'
    c.execute(q)

    #check data is valid
    q = 'SELECT school_name
         IF (school = ?, gender = ?)
         FROM schools'
    new  = c.execute(q, (school_name, gender))
    if len(new) > 0:
        conn.close()
        return [False, "School and gender already exists"]
    else:
        q = 'INSERT INTO schools (school_name, street_address, borough, zipcode, team, division, coach, manager, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        c.execute(q, (school_name, street_address, borough, zipcode, team, division, coach, manager, gender))
        conn.commit()
        conn.close()
        return [True, "Successful School Creation"]

######## CREATE EVENT ########

def create_event(school_home, home_score, school_away, away_score, date, time, game_id, status, address):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #create events table
    q = 'CREATE TABLE IF NOT EXISTS events (school_home TEXT, home_score INT, school_away TEXT, away_score INT, date TEXT, time TEXT, game_id INT, status TEXT, address TEXT)'
    c.execute(q)

    #check data is valid
    q = 'SELECT game_id
         IF (game_id = ?)
         FROM events'
    new  = c.execute(q, (game_id))
    if len(new) > 0:
        conn.close()
        return [False, "Event already exists"]
    else:
        q = 'INSERT INTO schools (school_home, home_score, school_away, away_score, date, time, game_id, status, address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        c.execute(q, (school_home, home_score, school_away, away_score, date, time, game_id, status, address))
        conn.commit()
        conn.close()
        return [True, "Successful Event Creation"]

######## CREATE PLAYER ########

def create_player(year, first_name, last_name, school, grad_year, player_type, game_id, matches, win, loss, touch, position):
    #set up connection
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    #create players table
    q = 'CREATE TABLE IF NOT EXISTS ?_players (year INT, player_id INT, first_name TEXT, last_name TEXT, school TEXT, grad_year INT, player_type TEXT, game_id INT, matches INT, win INT, loss INT, touch INT, position TEXT)'
    c.execute(q, str(year))

    q = 'SELECT COUNT(*) FROM ?_players'
    num_players = c.execute(q, str(year)).fetchone()[0]
    
    #need to check that player doesn't already exist

    #add player
    q = 'INSERT INTO players (year, player_id, first_name, last_name, school, grad_year, player_type, game_id, matches, win, loss, touch, position) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    c.execute(q, (year, num_players + 1, first_name, last_name, school, grad_year, player_type, game_id, matches, win, loss, touch, position))
    conn.commit()
    conn.close()
    return [True, "Successful Player Creation"]

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
