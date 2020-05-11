import models
import datetime
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

stocks = Blueprint('stocks', 'stocks')

# route - GET /stocks/all 
@stocks.route('/all')
def get_all_stockss():
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
