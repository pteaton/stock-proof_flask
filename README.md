# Stock Proof 

### Author
Patrick Eaton

### About
Do you play the stock market? Do you want to let people know about your successful stocks or warn others of stocks to avoid? Well then stockproof is for you! stockproof allows you to create and test stocks using the piotroski f-score to determine if the stock is worth pursuing, if the stock runs well on the f-score then upload it to the stock show page for other users to see!


### Technology Used
Cloudinary, CORS, Postgress SQL, Python-Flask, React & Sqlite

# Routes
### Users
	POST	/users/login – user login 
	POST	/users/register – user register
	GET	/users/logout – user logout
	PUT 	/users/<id> – user edit/update profile
	DELETE  /users/<id> - delete user profile

### Stocks
	GET	/mystocks – shows stocks
	POST	/stocks - create stock
	PUT	/stocks/<id> – edit/update stock 
	DELETE	/stocks/<id> – delete stock

### Screens
	GET 	/myscreens – shows user screens
	POST	/screens – create screen
	PUT 	/screens/<id> - edit/update screen
	DELETE	/screens/<id> - delete screen


# Models 
### User
	email = CharField(unique=True)
	username = CharField(unique=True)
	password = CharField()
	profile_pic = TextField()
	bio = TextField()

### Stock
	bad_management = CharField() – stable management,  low turnover mid/high positions
	balance_sheet = CharField() – assets, liabilities, net worth calculation	
	enterprise_life_cycle = TextField() – development, reinvestment for success		
	economic_moat = TextField() – competitive advantages	
	dividend_paying_stock = CharField() – business compounds wealth over time	
	earnings_stability = CharField() –  yes/no -- lowers chance of forecasting errors and risk	
	operating_efficiency = IntegerField() – Return on Assets = net income/assets
	creator = ForeignKeyField(User, backref=’stocks’) – cites the author of the stock
	date_posted = date(default=date.time.datetime.now) – time stock posted

## Piotroski F-Score Screen:  
Used to determines value of stock

Uses a binary pass/fail system 

Scored on a scale of 0 - 9

### Profitability: (4 points)
	return_on_asset =: IntegerField() 
	cash_flow_from_operations = IntegerField() 
	direction_of_return_on_assets = IntegerField() 
	accrual_accounting_check = IntegerField() 

### CapitalStructure: (3 points)
	direction_of_leverage = IntegerField() 
	direction_of_liquidity = IntegerField()  
	issue_stock = IntegerField()  	
	
### OperatingEfficiency: (2 points)
	direction_of_margin = IntegerField()  
	direction_of_asset_turnover = IntegerField()

### Stretch Goals
Users can upload a profile picture

Users can rate other stocks

Users can like other stocks

Stocks update using live data

### How to start app:
1) install python3
	
2) clone this repository in your terminal in a folder of your choosing, 
	
3) in that new folder run virtual .env -p python 3 in your terminal
	
4) now use source .env/bin/activate to run the virtual environment 

5) with (.env) in the terminal, run pip3 install -r requirement.txt 

6) then in the terminal enter pip3 freeze > requirements.txt 

7) now just enter python3 app.py in the new folder to run the app


