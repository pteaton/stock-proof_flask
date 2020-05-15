# Stock Proof 

### Author
Patrick Eaton

### About
Do you play the stock market? Do you want to let people know about your successful stocks or warn others of stocks to avoid? Well then stockproof is for you! Stockproof allows you to track certain stocks and add them to a portfolio for further study!



### Technology Used
CORS, Postgress SQL, Python-Flask, React & Sqlite

# Routes
### Users
	POST	/users/login – user login 
	POST	/users/register – user register
	GET	/users/logout – user logout
	PUT 	/users/<id> – user edit/update profile
	DELETE  /users/<id> - delete user profile

### Stocks
	GET	/mystocks – shows stocks
	GET /allstocks - shows all stocks
	POST	/stocks - create stock
	PUT	/stocks/<id> – edit/update stock 
	DELETE	/stocks/<id> – delete stock

# Models 
### User
	email = CharField(unique=True)
	username = CharField(unique=True)
	password = CharField()
	bio = TextField()

### Stock
	symbol = CharField()
	name = CharField()	
	user = ForeignKeyField(User, backref='stocks', on_delete="CASCADE") 
	date_added = DateTimeField(default=datetime.datetime.now)



# Stretch Goals
Piotroski F-Score Screens stocks for value

Users can upload a profile picture

Users can like other stocks

Stocks update using live data


# How to start app:
1) install python3
	
2) clone this repository in your terminal in a folder of your choosing, 
	
3) in that new folder run virtual .env -p python 3 in your terminal
	
4) now use source .env/bin/activate to run the virtual environment 

5) with (.env) in the terminal, run pip3 install -r requirement.txt 

6) then in the terminal enter pip3 freeze > requirements.txt 

7) now just enter python3 app.py in the new folder to run the app


