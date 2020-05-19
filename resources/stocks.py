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
### Create stocks w/ name, symbol, logged in user [CHECKMARK]
### Show stocks - GET route for /all and /<id> (for user specific stocks) [CHECKMARK; got stock for fatima]
#######

#######
### IN REACT !!
### Landing page for showing stocks both /all and /<id> 
### Plot stocks on plot, create search page to add stock to porfolio
### then build way to map both user and  found stocks

# index route for stocks - GET /api/v1/
@stocks.route('/', methods=['GET'])
@login_required
def stocks_index():
	
	current_user_stock_dicts = [model_to_dict(stock) for stock in current_user.stocks]
	
	for stock_dict in current_user_stock_dicts:
		stock_dict['user'].pop('password')
	
	print(current_user_stock_dicts)

	return jsonify({
		'data': current_user_stock_dicts,
		'message': f"Successfully found {len(current_user_stock_dicts)} stocks",
		'status': 200
	}), 200



# create stock route - POST api/v1/stocks/add 
@stocks.route('/add', methods=['POST'])
@login_required
def create_stock():
	# edit to change from user input to api input
	payload = request.get_json()
	# call api
	new_stock = models.Stock.create(
		symbol=payload['symbol'],
		name=payload['name'],
		user=current_user.id,
	)

	stock_dict = model_to_dict(new_stock)

	print(stock_dict)

	stock_dict['user'].pop('password')

	return jsonify(
		data=stock_dict,
		message=f"Successfully created {stock_dict['name']}!!",
		status=201
	), 201

# show all stocks - GET api/v1/stocks/all
@stocks.route('/all', methods=['GET'])
def display_all_stocks():
	stocks = models.Stock.select()

	stock_dicts = [ model_to_dict(stock) for stock in stocks]
	for stock_dict in stock_dicts:
		stock_dict['user'].pop('password')

	return jsonify (
		data=stock_dicts,
		message=f"Found {len(stocks)} here",
		status=200
	), 200


# show stock - GET api/v1/stocks/<id>
@stocks.route('/<id>', methods=['GET'])
def show_stock(id):
	stock = models.Stock.get_by_id(id)

	if not current_user.is_authenticated:
		return jsonify(
			data={
				'symbol': stock.symbol,
				'name': stock.name,
			},
			message=f"Registered users can see more info about this stock",
			status=200
		), 200

	else: 
		stock_dict = model_to_dict(stock)
		stock_dict['user'].pop('password')

		if stock.date_added != current_user.id:
			stock_dict.pop('date_added')

		return jsonify(
			data=stock_dict,
			message=f"Found stock with id {id}",
			status=200
		), 200


# destroy stock route  - DELETE api/v1/stocks/<id>
@stocks.route('/<id>', methods=['DELETE'])
@login_required
def delete_stock(id):

		stock_to_delete = models.Stock.get_by_id(id)

		if current_user.id == stock_to_delete.user.id:

			stock_to_delete.delete_instance()

			return jsonify (
				data={},
				message="Successfully deleted stock",
				status=201
			), 201

		else:

			return jsonify (
				data={},
				message="Only original poster can delete",
				status=403
			), 403

# need to add edit/update?
@stocks.route('/<id>', methods=['PUT'])
@login_required
def edit_stock(id):
	payload=request.get_json()
	stock_to_edit = models.Stock.get_by_id(id)

	print(payload,"This is the payload man")
	print(stock_to_edit, "stock to edit right here tho")
	if current_user.id == stock_to_edit.user.id:
		stock_to_edit.f_score=payload['f_score']

		stock_to_edit.save()

		stock_to_edit_dict = model_to_dict(stock_to_edit)
		stock_to_edit_dict['user'].pop('password')

		return jsonify (
			data=stock_to_edit_dict,
			message="Successfully edited your stock",
			status=201
		), 201

	else:

		return jsonify (
			data={},
			message="That is not your stock, you cannot edit it",
			status=403
		), 403 

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


