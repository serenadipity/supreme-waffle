# supreme-waffle
Fencing Statistics Website

#Members
| Member         | Github                                           | Role         |
|----------------|--------------------------------------------------|--------------|
| Serena Chan    | [@serenadipity](https://github.com/serenadipity) | front-end    |
| Kathy Wang     | [@kwangaroo](https://github.com/kwangaroo)       | back-end     |
| Sammi Wu Leung | [@sammiwl](https://github.com/sammiWL)           | middle-front |
| Alice Xue      | [@alicexue](https://github.com/alicexue)         | middle-back  |

#Things To Install
* Flask
* SQL

#Log
|   Date   | Who | Description  |
|----------|-----|--------------|
|05/12/2016|Group|We met with our client, Nicholas Yang. |
|05/13/2016|Group| We looked at the PSAL website to develop ideas. |
|05/16/2016|Group|We began basic website design and learned more about the subject. |
|05/17/2016|Group| We planned out the timeline of the project, created the color scheme, worked on databases, and went on an immersive tour of the subject. |
|05/18/2016|Group| We presented our plan for the website and the toolkits we are using. We also made a font shortlist.|
|05/19/2016|Group| We did more planning for database.|
|05/20/2016|KW| We worked on creating the databases.|
|05/21/2016|KW,SWL, AX| We completed user registration and login, as well as school registration and profiles. We worked on player registration and profiles. (func: register, authenticate, valid_user, create_player, create_school)|
|05/22/2016|SWL| We completed school profile presentation and worked on player registration and profiles. (func: get_school, get_distinct_school, get_players*)|
|05/22/2016|SC|We worked on the look and feel of the user interface on the login/registration pages|
|05/23/2016|SWL| We worked on improving functionality of registration and getting basic ideas up. (route: directory)|
|05/24/2016|AX| We worked on get data from the database. (func: get_players_by_year_and_school, get_gamescores_by_school)|
|05/25/2016|KW, AX| We worked on logging individual touches, recording scores from each bout, and calculating player indicators. We also worked on displaying player information and scores in school profiles.|
|05/25/2016|SWL| We worked on getting bar charts to work w/ D3.|
|05/26/2016|Group| We met with Nicholas Yang to have our second client meeting. We resolved issues such as who gets to control the data being inputted. We concluded that the data would be based on the honor system or a Super User may edit that data. | 
|05/26/2016|KW| We finished editing and testing the individual functions that were made and began working on line graphs. |
|05/26/2016|SWL| We modified the player registration to fit our purposes.|
|05/27/2016|AX| We began writing functions to edit school profiles.|
|05/30/2016|SWL| We got the uploading/displaying of pictures to work by directly linking it to the file system instead of storing it in a database since the pictures would be large and no high security is needed.|
|05/30/2016|SC | We further improved the look of the user interface. |
|05/31/2016|AX| We are able to edit school and player profiles.|
|06/02/2016|AX| We worked on event registration.|
|06/03/2016|AX| We began working on inputting statistics (created the forms).|
|06/05/2016|AX| We finished inputting of stats from forms and inputted to the database.|
|06/07/2016|SWL| Crunch Time. We added many things such as events input and indicator ranking. |

#Deployment Guide 
1. Set up a DigitalOcean droplet to the desired size. 
2. SSH into the IP of the droplet. 
3. Create a new user on the droplet with <code>useradd -r -m -s [NAME OF USER]</code>.
4. While still on the root account, install pip. 
5. Install virtualenv by running <code>pip install virtualenv.</code>
6. Also, install git and nginx by running <code>apt-get install git</code> and <code>apt-get install nginx</code>, respectively.
7. Switch over to the deployment account by running <code> su - [name] </code>
8. Clone the project repo by running <code>git clone https://github.com/serenadipity/supreme-waffle.git </code>
9. cd into the repo. 
10. Set up the virtual environment with <code>virtualenv venv</code>.
11. Activate it by running <code>source venv/bin/activate</code>.
12. In the virtual environment, pip install gunicorn, flask, and sql. 
13. Do Issue #1 in <a href="https://blog.marksteve.com/deploy-a-flask-application-inside-a-digitalocean-droplet/">the guide that guided this guide.</a>
14. Run script_maker.py
14. Run <code>gunicorn -D app:app</code>
15. Navigate to the droplet on your browser and check out the site!
