import models
import datetime
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

stocks = Blueprint('stocks', 'stocks')

# stock api - volatility of stock/realtime data
api_key = 'EIRKD54AJXO1NRSD'

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT', interval='60min', outputsize='compact')
print(data)
			# variable in symbol, use to search, route for stock
i = 1
while i==1:
	data, meta_data = ts.get_intraday(symbol='MSFT', interval='60min', outputsize='compact')
	time.sleep(60)

close_data = data['4. close']
percentage_change = close_data.pct_change()

print(percentage_change)

last_change = percentage_change[-1]

if abs(last_change) > 0.0004:
	print("MSFT Alert:" + last_change)

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


# route - GET /stocks/all - all stocks
@stocks.route('/all')
def get_all_stocks():
	stocks = models.Stock.select()

	stock_dicts = [model_to_dict(stock) for stock in stocks]

	for stock_dict in stock_dicts:
		stock_dict['poster'].pop('password')
		if not current_user.is_authenticated:
			stock_dict.pop('poster')

	return jsonify({
		'data': stock_dicts,
		'message': f"Successfully found {len(stock_dicts)} stocks",
		'status': 200

	}), 200

# route - POST /stocks/ - create stock
@stocks.route('/', methods=['POST'])
@login_required
def create_stock():
	
	payload = request.get_json()

	new_stock = models.Stock.create(
		company_name=payload['company_name'],
		market_cap=payload['market_cap'],
		beta=payload['beta'],
		stock_open=payload['stock_open'],
		previous_close=payload['previous_close'],
		price_to_earnings_ratio=payload['price_to_earnings_ratio'],
		earnings_per_share=payload['earnings_per_share'],
		poster=current_user.id,
		date_posted=datetime.datetime.now()
	)

	stock_dict = model_to_dict(new_stock)

	print(stock_dict)

	stock_dict['poster'].pop('password')

	return jsonify(
		data=stock_dict,
		message="Successfully created a stock!!",
		status=201
	), 201


# update stock route
@stocks.route('/<id>', methods=['PUT'])
@login_required
def update_stock(id):

	payload = request.get_json()
	stock_to_update = models.Stock.get_by_id(id)
	print(type(stock_to_update))
	print(stock_to_update)

	if stock_to_update.poster.id == current_user.id:

		if 'company_name' in payload:
			stock_to_update.company_name = payload['company_name']
		if 'market_cap' in payload:
			stock_to_update.market_cap = payload['market_cap']
		if 'beta' in payload:
			stock_to_update.beta = payload['beta']
		if 'stock_open' in payload:
			stock_to_update.stock_open = payload['stock_open']
		if 'previous_close' in payload:
			stock_to_update.previous_close = payload['previous_close']
		if 'price_to_earnings_ratio' in payload:
			stock_to_update.price_to_earnings_ratio = payload['price_to_earnings_ratio']
		if 'earnings_per_share' in payload:
			stock_to_update.earnings_per_share = payload['earnings_per_share']

		stock_to_update.save()
		updated_stock_dict = model_to_dict(stock_to_update)
		updated_stock_dict['poster'].pop('password')

		return jsonify(
			data=updated_stock_dict,
			message=f"Successfully updated your stock with id {id}",
			status=200
		), 200

	else:
		return jsonify(
			data={
				'error': '403 Forbidden'
			},
			message="Username doesn't match stock id. Only creator can update",
			status=403
		), 403


# show stocks
@stocks.route('/<id>', methods=['GET'])
def show_stock(id):
	stock = models.Stock.get_by_id(id)

	if not current_user.is_authenticated:
		return jsonify(
			data={
				'company_name': stock.company_name,
				'market_cap': stock.market_cap,
				'beta': stock.beta,
				'stock_open': stock.stock_open,
				'previous_close': stock.previous_close,
				'price_to_earnings_ratio': stock.price_to_earnings_ratio,
				'earnings_per_share': stock.earnings_per_share
			},
			message="Registered users can see more info about this stock",
			status=200
		), 200

	else: 
		stock_dict = model_to_dict(stock)
		stock_dict['poster'].pop('password')

		if stock.posted_by.id != current_user.id:
			stock_dict.pop('date_posted')

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



