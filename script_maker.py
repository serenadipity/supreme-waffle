
from datas import *
from random import randint


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
        create_player(2016, gf_names[randint(0, len(gf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[0], grad_year[randint(0, len(grad_year) - 1)], player_types[0], "starter")
        create_player(2016, gf_names[randint(0, len(gf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[0], grad_year[randint(0, len(grad_year) - 1)], player_types[1], "starter")
        create_player(2016, bf_names[randint(0, len(bf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[1], grad_year[randint(0, len(grad_year) - 1)], player_types[0], "starter")
        create_player(2016, bf_names[randint(0, len(bf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[1], grad_year[randint(0, len(grad_year) - 1)], player_types[1], "starter")
    for j in range(randint(3, 10)):
        create_player(2016, gf_names[randint(0, len(gf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[0], grad_year[randint(0, len(grad_year) - 1)], player_types[0], "regular")
        create_player(2016, gf_names[randint(0, len(gf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[0], grad_year[randint(0, len(grad_year) - 1)], player_types[1], "regular")
        create_player(2016, bf_names[randint(0, len(bf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[1], grad_year[randint(0, len(grad_year) - 1)], player_types[0], "regular")
        create_player(2016, bf_names[randint(0, len(bf_names) - 1)], last_names[randint(0, len(last_names) - 1)], school_names[i], genders[1], grad_year[randint(0, len(grad_year) - 1)], player_types[1], "regular")
