
from datas import *
from random import randint

create_all_tables()

######### MAKE SCHOOLS #########
school_names = ["Kathy Wang Clown School for Clowns", "Sammi's Bird School for Birds", "Kelly School of Passive Aggressiveness", "Alice School for Really Pretty Hidden Profile Pictures", "Serena Chan's Fencing School"]
addresses = ["7656 Aliquam Street", "3916 Mauris St.", "420 Amet Ave", "6966 Felis. Avenue", "2253 Urna Road"]
boroughs = ["Brooklyn", "Bronx", "Staten Island", "Manhattan", "Queens"]
zips = [60904, 01007, 15691, 61030, 27931]
teams = ["Bunnies","Pigs", "Gazelles", "Chipmunk", "Antelopes", "Badgers", "Finches", "Puppies", "Alligators", "Bulls", "Bats"]
divisions = [1, 2, 3]
coaches = ["Denton Molina", "Amena Huffman", "Willa Riley", "Sybill Haney", "Kareem Gates", "Mira Larsen", "Thomas Oneal", "Erin Oliver", "Evelyn Sweet", "Angelica Snider"]
managers = ["Herman Sargent", "David Drake", "Jasmine Wolf", "Giselle Meyer", "Vernon Mccoy", "Tara Larsen", "Imelda Morin", "Avram Cruz", "Alden Hayden", "Fatima Mills"]
genders = ["Girls", "Boys"]

for i in range(5):
    create_school(school_names[i], addresses[i], boroughs[i % 5], zips[i], teams[2 * i], divisions[i % 3], coaches[2 * i], managers[2 * i], genders[0]) 
    create_school(school_names[i], addresses[i], boroughs[i % 5], zips[i], teams[2 * i + 1], divisions[i % 3], coaches[2 * i + 1], managers[2 * i + 1], genders[1]) 

for i in range(5):
    add_school_image(school_names[i], genders[0], ("_".join(school_names[i].split(" ")) + "_" + genders[0] + ".jpg"))
    add_school_image(school_names[i], genders[1], ("_".join(school_names[i].split(" ")) + "_" + genders[1] + ".jpg"))

######### MAKE PLAYERS #########
gf_names = ["Priscilla", "Serena", "Bertha", "Keiko","Tamara","Kiayada","Octavia","Joelle","Medge","Eden","Demetria","Jayme","Shoshana","Rhonda","Abigail","Lynn","Eugenia","Melanie", "Mikayla","Rebecca", "Carissa", "Sammi", "Kathy", "Alice", "Samantha", "Lily", "Rose", "Yuxin", "Kathy", "Rina", "Jessie", "Sam", "Anna", "Andrea", "Madeline"]
bf_names = ["Howard", "Nehru","Rigel","Griffith","Hyatt","Barry","Elmo","Keane","Edan","Giacomo","Denton","Tyrone","Ciaran","Colorado","Colorado","Phelan","Victor","Mannix","Griffin","Driscoll", "Aaron", "Hing", "Channing", "Peter", "Mosaab", "Will", "Jesse", "Victor", "Stephan", "Sebastian", "Adam"]
last_names = ["Mcintosh","Yang","Randall","Bennett","Stafford","Hodges","Whitney","Tucker","Mccray","Hodges","Zhang","Rodriguez","Jacobs","Coffey","Randolph","Nolan","Fulton","Horne","Tillman","Figueroa","Ellis","Crawford","Ball","Qing","Garza","Craig","Fry","Russell","Shaffer","Armstrong","Galloway","Bradford","Smith","Greene","Hewitt","Macias","Norton","Hoffman","Johnson","Pruitt"]
grad_year = [2016, 2017, 2018, 2019]
player_types = ["Foil","Epee"]

for i in range(5):
    for j in range(3):
        create_player(2016, gf_names[randint(0, len(gf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[0], grad_year[randint(0, len(grad_year) - 1)], player_types[0], "Starter", True)
        create_player(2016, gf_names[randint(0, len(gf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[0], grad_year[randint(0, len(grad_year) - 1)], player_types[1], "Starter", True)
        create_player(2016, bf_names[randint(0, len(bf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[1], grad_year[randint(0, len(grad_year) - 1)], player_types[0], "Starter", True)
        create_player(2016, bf_names[randint(0, len(bf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[1], grad_year[randint(0, len(grad_year) - 1)], player_types[1], "Starter", True)
    for j in range(5):
        create_player(2016, gf_names[randint(0, len(gf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[0], grad_year[randint(0, len(grad_year) - 1)], player_types[0], "Regular", True)
        create_player(2016, gf_names[randint(0, len(gf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[0], grad_year[randint(0, len(grad_year) - 1)], player_types[1], "Regular", True)
        create_player(2016, bf_names[randint(0, len(bf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[1], grad_year[randint(0, len(grad_year) - 1)], player_types[0], "Regular", True)
        create_player(2016, bf_names[randint(0, len(bf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[1], grad_year[randint(0, len(grad_year) - 1)], player_types[1], "Regular", True)


######### MAKE EVENTS #########

for i in range(30):
    schoolH = school_names[randint(0, len(school_names) - 1)]
    schoolA = school_names[randint(0, len(school_names) - 1)]
    while (schoolA == schoolH):
        schoolA = school_names[randint(0, len(school_names) - 1)]
    date = "0" + str(randint(2, 6)) + "/" + str(randint(10, 31)) + "/2016"
    time = "3:30 PM"
    address = schoolH
    game = randint(10000, 40000)
    
    if randint(0, 100) == 0:
        status = "postponed to another time"
    else:
        status = "on time"
    gender = genders[randint(0, 1)]
    create_event(schoolH, schoolA, date, time, game, status, address, gender)

    for k in range(0,2):
        if k == 0:
            gametype = "Foil"
        else:
            gametype = "Epee"
        if gender == "Girls":
            playersH = get_team_players(2016,schoolH,gametype,"Girls")
            playersA = get_team_players(2016,schoolA,gametype,"Girls")
            gender = "Girls"
        else:
            playersH = get_team_players(2016,schoolH,gametype,"Boys")
            playersA = get_team_players(2016,schoolA,gametype,"Boys")
            gender = "Boys"
        p1 = playersH[randint(1,len(playersH)-1)][1]
        p2 = playersA[randint(1,len(playersA)-1)][1]
        for i in range(1,10):
            home_touches = randint(0,50)
            home_score = randint(0,30)
            away_touches = randint(0,50)
            away_score = randint(0,30)
            create_ind(schoolH, p1, home_touches, home_score, schoolA, p2, away_touches, away_score, date, gametype, game, i, address, 2016, gender)
    
