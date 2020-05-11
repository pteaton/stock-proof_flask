import datetime
from flask_login import UserMixin
from playhouse.db_url import connect

class User(UserMixin, Model):
	username=CharField(unique=True)
	email=CharField(unique=True)
	password=CharField()
	bio=TextField()

	class Meta:
		database = DATABASE


class Stock(Model):
	company_name=CharField()
	market_cap=IntegerField()
	beta=IntegerField()
	stock_open=IntegerField()
	previous_close=IntegerField()
	price_to_earnings_ratio=IntegerField()
	earnings_per_share=IntegerField()
	poster=ForeignKeyField(User, backref='stocks')
	date_posted=date(default=date.time.datetime.now)

	class Meta:
		database = DATABASE


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

	class Meta:
		database = DATABASE



def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Review, Screen, Tracker], safe=True)
	print("DB connected and created tables")
	DATABASE.close()