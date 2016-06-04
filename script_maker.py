
from datas import *

school_names = ["Kathy Wang Clown School for Clowns", "Sammi's Bird School for Birds", "Kelly School of Passive Aggressiveness", "Alice School for Really Pretty Hidden Profile Pictures", "Serena Chan's Fencing School"]
addresses = ["7656 Aliquam Street", "3916 Mauris St.", "420 Amet Ave", "6966 Felis. Avenue", "2253 Urna Road"]
boroughs = ["Brooklyn", "Bronx", "Staten Island", "Manhattan", "Queens"]
zips = [60904, 01007, 15691, 61030, 27931]
teams = ["Bunnies","Pigs", "Gazelles", "Chipmunk", "Antelopes", "Badgers", "Finches", "Puppies", "Alligators", "Bulls", "Bats"]
divisions = [1, 2, 3]
coaches = ["Denton Molina", "Amena Huffman", "Willa Riley", "Sybill Haney", "Kareem Gates", "Mira Larsen", "Thomas Oneal", "Erin Oliver", "Evelyn Sweet", "Angelica Snider"]
managers = ["Herman Sargent", "David Drake", "Jasmine Wolf", "Giselle Meyer", "Vernon Mccoy", "Tara Larsen", "Imelda Morin", "Avram Cruz", "Alden Hayden", "Fatima Mills"]
genders = ["Boys", "Girls"]

for i in range(5):
    create_school(school_names[i], addresses[i], boroughs[i % 5], zips[i], teams[2 * i], divisions[i % 3], coaches[2 * i], managers[2 * i], genders[0]) 
    create_school(school_names[i], addresses[i], boroughs[i % 5], zips[i], teams[2 * i + 1], divisions[i % 3], coaches[2 * i + 1], managers[2 * i + 1], genders[1]) 

for i in range(5):
    add_school_image(school_names[i], genders[0], ("_".join(school_names[i].split(" ")) + "_" + genders[0] + ".jpg"))
    add_school_image(school_names[i], genders[1], ("_".join(school_names[i].split(" ")) + "_" + genders[1] + ".jpg"))

