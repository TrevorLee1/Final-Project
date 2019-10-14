# Final Project - Trevor and Tarun

This is a debate website created using Flask. It serves as an information and resource repository for aspiring debaters

This is a very simple web application made using Python3 with the module Flask and some simple HTML templates.
The app has a few features:

1. Registration and login functions
2. Raffles Debaters information/"about"
3. Weekly digest (Weekly article about interesting historical or current affairs)
4. Debate motion repository
    4a. Categorisation based on motion type (philosophical, retrospective or policy)
    4b. Categorisation based on motion origin (from training or from tournaments)
    4c. Debate details (Definitions, ideal cases/arguments and stances)
5. Search function for motions
6. Admin function that limits users that can edit the website
    6a. Admins are able to add new motions
    6b. Admins are able to edit debate details
    6c. Admins can be granted to teachers, coaches, CCA EXCO etc via grant_admin.sql, which contains SQL code to alter the database to reflect admin status accordingly

We have not used any external libraries for this project. This the modules/imports you will require are almost the same as Summative 3, namely:

Flask
Flask-Session
psycopg2
SQLAlchemy
os
requests

To begin with, head over to requirements.txt and ensure that you have all the requirements to run this programme.

After that, you will need to set 2-3 environment variables after navigating to the directory that application.py is in.
These are the relevant commands:

1a (If using Powershell) $env:FLASK_APP = "application.py"
1b (If using Command Prompt) set FLASK_APP = application.py
1c (If using Mac) export FLASK_APP = application.py

(Optional)
2a (If using Powershell) $env:FLASK_DEBUG = 1
2b (If using Command Prompt) set FLASK_DEBUG = 1
2c (If using Mac) export FLASK_DEBUG = 1

(IMPORTANT - This is the database with all the relevant data in it )
3a (If using Powershell) $env:DATABASE_URL = postgres://clkvoqtbcnumbx:0c56486250dede96437d9a1e85f89bff2f16644be27472ceab83a361e99cbc68@ec2-23-21-148-223.compute-1.amazonaws.com:5432/d60qv0tumutcju
3b (If using Command Prompt) set DATABASE_URL = postgres://clkvoqtbcnumbx:0c56486250dede96437d9a1e85f89bff2f16644be27472ceab83a361e99cbc68@ec2-23-21-148-223.compute-1.amazonaws.com:5432/d60qv0tumutcju
3c (If using Mac) export DATABASE_URL = postgres://clkvoqtbcnumbx:0c56486250dede96437d9a1e85f89bff2f16644be27472ceab83a361e99cbc68@ec2-23-21-148-223.compute-1.amazonaws.com:5432/d60qv0tumutcju

Finally, to begin running the application, just input "flask run" (excluding the inverted commas) and copy the link provided in the console
onto a browser's URL bar. From there, you will be guided to the website's index page where you need only to register and login before being able to use the website!

Other notes:
The SQL file grant_admin.sql contains SQL code to grant any user admin status
Video link can be found in the Video.txt file.

Credits:
Tarun (Html, debugging)
Trevor (Flask, some html, database management, debugging, readme, annotations, video)

Disclaimers:
This is still a work in progress and there may be many other features to come. We would also like to use it for RI's Debate Club if possible.
PEP8 style guide has not been adhered to, as some of the lines of code are too long to be shortened. We hope that it is still fairly readable, however

Potential/Unimplemented features:
1. Tabbing software [Tabbycat?] for users to tabulate adjudicators' marks and scores when hosting a tournament (British Parliament/World Schools Debate Championship/Singapore Secondary School Debate Championship format)
2. Seeding system to determine matchups, also for use when hosting tournaments
3. Club announcements
4. More polish on details, e.g contact numbers of teachers etc.
5. More resources
6. Feedback/tellonym system for public

Apologies for the late submission
