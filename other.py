####### annoying function sammi wants me to write. #####
def get_team_indicators(year, school, gender, gametype):
    #set up connection YET AGAIN
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    indicator_list = []
    
    q = "SELECT first_name, last_name, id FROM players_" + str(year) + "WHERE school = ? AND player_type = ? AND gender = ?"
    print c.execute(q, (school, gametype, gender)).fetchall()
    
    #get name
    
#get_team_indicators(2016, "Stuyvesant High School", "Boys Team", "Epee")



######## GET PLAYER BY YEAR, SCHOOL, TYPE, GENDER #######
def get_team_players(year, school, gametype, gender):
    #set up connection..... again.....
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    q = "SELECT * FROM players_" + str(year) + "WHERE school = ? AND player_type = ? AND gender = ?"
    players = c.execute(q, (school, gametype, gender)).fetchall()

    return players

get_team_players(2016, "Stuyvesant High School", "Epee", "Boys Team")


