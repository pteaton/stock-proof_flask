import os
from peewee import *
import datetime
from flask_login import UserMixin
from playhouse.db_url import connect

DATABASE = SqliteDatabase('stocks.sqlite')
DATABASE = SqliteDatabase('screens.sqlite')


class User(UserMixin, Model):
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField()
	bio=TextField()

	class Meta:
		database=DATABASE


class Stock(Model):
	company_name = CharField()
	stock_open = IntegerField()
	stock_high = IntegerField()
	stock_low = IntegerField()
	previous_close = IntegerField()
	stock_volume = IntegerField()	
	poster = ForeignKeyField(User, backref='stocks', on_delete="CASCADE") 
	date_posted = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database=DATABASE


class Screen(Model):
	return_on_asset=IntegerField()
	cash_flow_from_operations=IntegerField()
	direction_of_return_on_assets=IntegerField()
	accrual_accounting_check=IntegerField()
	direction_of_leverage=IntegerField()
	direction_of_liquidity=IntegerField()
	issue_stock=IntegerField()
	direction_of_margin=IntegerField()
	direction_of_asset_turnover=IntegerField()
	poster=ForeignKeyField(User, backref='screens')
	date_posted=DateTimeField(default=datetime.datetime.now)

	class Meta:
		database=DATABASE



def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Stock, Screen], safe=True)
	print("DB connected and created tables")
	DATABASE.close()