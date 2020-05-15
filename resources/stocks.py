import models
import datetime
import pandas as pd
import time
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

stocks = Blueprint('stocks', 'stocks')

# stock api from alpha vantage - volatility of stock/realtime data
# api_key = 'EIRKD54AJXO1NRSD'


#######
### Create stocks w/ name, symbol, logged in user
### Show stocks - GET route for /all and /<id> (for user specific stocks)
#######

#######
### IN REACT !!
### Landing page for showing stocks both /all and /<id> 
### Plot stocks on plot, create search page to add stock to porfolio
### then build way to map both user and  found stocks

# route - GET /api/v1/stocks/ - mystocks
@stocks.route('/', methods=['GET'])
@login_required
def stocks_index():
	
	current_user_stock_dicts = [model_to_dict(stock) for stock in current_user.stocks]
	
	for stock_dict in current_user_stock_dicts:
		stock_dict['poster'].pop('password')
	
	print(current_user_stock_dicts)

	return jsonify({
		'data': current_user_stock_dicts,
		'message': f"Successfully found {len(current_user_stock_dicts)} stocks",
		'status': 200
	}), 200



# route - POST /stocks/ - create stock
@stocks.route('/', methods=['POST'])
@login_required
def create_stock():
	# edit to change from user input to api input
	payload = request.get_json()
	# call api
	new_stock = models.Stock.create(
		symbol=payload['symbol'],
		name=payload['name'],
		user=current_user.id,
		date_added=datetime.datetime.now()
	)

	stock_dict = model_to_dict(new_stock)

	print(stock_dict)

	stock_dict['user'].pop('password')

	return jsonify(
		data=stock_dict,
		message="Successfully created a stock!!",
		status=201
	), 201




# show stocks
@stocks.route('/<id>', methods=['GET'])
def show_stock(id):
	stock = models.Stock.get_by_id(id)

	if not current_user.is_authenticated:
		return jsonify(
			data={
				'symbol': stock.symbol,
				'name': stock.name,
			},
			message="Registered users can see more info about this stock",
			status=200
		), 200

	else: 
		stock_dict = model_to_dict(stock)
		stock_dict['user'].pop('password')

		if stock.posted_by.id != current_user.id:
			stock_dict.pop('date_added')

		return jsonify(
			data=stock_dict,
			message=f"Found stock with id {id}",
			status=200
		), 200


# route to destroy stock
@stocks.route('/<id>', methods=['DELETE'])
@login_required
def delete_stock(id):

	try:

		stock_to_delete = models.Stock.get_by_id(id)

		if stock_to_delete.posted_by.id == current_user.id:
			stock_to_delete.delete_instance()

			return jsonify(
				data={},
				message=f"Successfully deleted stock with id {id}",
				status=200
			), 200

		else:

			return jsonify(
				data={
					'error': '403 Forbidden'
				},
				message="Username doesn't match stock id. Only OP can delete",
				status=403
			), 403

	except models.DoesNotExist:
		return jsonify(
			data={
				'error': '404 Not Found'
			},
			message="Sorry, but there is no record of a stock with this ID here",
			status=404
		), 404

@stocks.route('/mystocks', methods=['GET'])
@login_required
def my_stocks():
	
	current_user_dict = model_to_dict(current_user)

	current_user_stocks = [model_to_dict(stocks) for stocks in current_user.stocks]

	return jsonify(
		data=current_user_stocks,
		message="Found your stocks",
		status=200
	), 200


