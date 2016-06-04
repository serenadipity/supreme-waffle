
from datas import *

school_names = ["Kathy Wang Clown School for Clowns", "Bird School for Birds", "Kelly School of Passive Aggressiveness", "Alice School for Really Pretty Hidden Profile Pictures", "Serena Chan's Fencing School", "The Awesome School"]
addresses = ["7656 Aliquam Street", "3916 Mauris St.", "420 Amet Ave", "6966 Felis. Avenue", "2253 Urna Road", "9357 Sit Ave"]
boroughs = ["Brooklyn", "Bronx", "Staten Island", "Manhattan", "Queens"]
zips = [60904, 01007, 15691, 61030, 27931, 62548]
teams = ["Bunnies","Pigs", "Gazelles", "Chipmunk", "Antelopes", "Badgers", "Finches", "Puppies", "Alligators", "Bulls", "Bats", "Mules"]
divisions = [1, 2, 3]
coaches = ["Denton Molina", "Amena Huffman", "Willa Riley", "Sybill Haney", "Kareem Gates", "Mira Larsen", "Thomas Oneal", "Erin Oliver", "Evelyn Sweet", "Angelica Snider", "Aline Patrick", "Wing Mooney", "Petra Patel"]
managers = ["Herman Sargent", "David Drake", "Jasmine Wolf", "Giselle Meyer", "Vernon Mccoy", "Tara Larsen", "Dale Duke", "Troy Bryan", "Imelda Morin", "Avram Cruz", "Alden Hayden", "Fatima Mills"]
genders = ["Boys Team", "Girls Team"]

for i in range(6):
    create_school(school_names[i], addresses[i], boroughs[i % 5], zips[i], teams[2 * i], divisions[i % 3], coaches[2 * i], managers[2 * i], genders[0]) 
    create_school(school_names[i], addresses[i], boroughs[i % 5], zips[i], teams[2 * i + 1], divisions[i % 3], coaches[2 * i + 1], managers[2 * i + 1], genders[1]) 
