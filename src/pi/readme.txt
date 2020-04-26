CSCI991 Project Spring 2019, UOW
Team B

by: pt882@uowmail.edu.au, 2020-04-26.

--------------------------------------------------------------------------------

Project Name: Pi

Deployment:
	1) Python:
		1.1) Install Python3.7
		1.2) Install Lib:
			Flask (flask_sqlalchemy flask-mail)
			
	2) Setting the environment variables:
		MAIL_USERNAME="your email account"
		MAIL_PASSWORD="the password your email account"
		
	3) Create the databse pi.sqlite3 using sql script pi.sqlite3.sql
	
	4) Setting the firewall to allow the system accesses the working port such as 80 or you named.
	
	5) For a production environment, should use a strong web server such as
   Apache instead of the build-in web server of Flask.

	6) Start the web server (Apache) or app (build-in server)