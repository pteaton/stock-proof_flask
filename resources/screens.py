import models
import datetime
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required


screens = Blueprint('screens', 'screens')

# screen index - GET /screens/
@screens.route('/', methods=['GET'])
@login_required
def screens_index():
	
	current_user_screen_dicts = [model_to_dict(screen) for screen in current_user.screens]

	for screen_dict in current_user_screen_dicts:
		screen_dict['poster'].pop('password')

	print(current_user_screen_dicts)

	return jsonify({
		'data': current_user_screen_dicts,
		'message': f"Successfully found {len(current_user_screen_dicts)} screens",
		'status': 200
	}), 200


# show all screens - GET /screens/all
@screens.route('/all')
def get_all_screens():

	screens = models.Screen.select()

	screen_dicts = [model_to_dict(screen) for screen in screens]

	for screen_dict in screen_dicts:
		screen_dict['poster'].pop('password')
		if not current_user.is_authenticated:
			screen_dict.pop('poster')

	return jsonify({
		'data': screen_dicts,
		'message': f"Successfully found {leng(screen_dicts)} screens",
		'status': 200
	}), 200


# create screen - POST /screens/add
@screens.route('/add', methods=['POST'])
@login_required
def create_screen():

	payload = request.get_json()

	new_screen = models.Screen.create(
		return_on_assets=payload['return_on_assets'],
		cash_flow_from_operations=payload['cash_flow_from_operations'],
		direction_of_return_on_assets=payload['direction_of_return_on_assets'],
		accrual_accounting_check=payload['accrual_accounting_check'],
		direction_of_leverage=payload['direction_of_leverage'],
		direction_of_liquidity=payload['direction_of_liquidity'],
		issue_stock=payload['issue_stock'],
		direction_of_margin=payload['direction_of_margin'],
		direction_of_asset_turnover=payload['direction_of_asset_turnover']

	)

	screen_dict = model_to_dict(new_screen)

	print(screen_dict)

	screen_dict['poster'].pop('password')

	return jsonify(
		data=screen_dict,
		message="Successfully created a stock screen",
		status=201
	), 201
	

# update screen - PUT /<id>/
@screens.route('/<id>', methods=['PUT'])
@login_required
def update_screen(id):

	payload = request.get_json()
	screen_to_update = models.Screen.get_by_id(id)
	print(type(screen_to_update))
	print(screen_to_update)

	if screen_to_update.poster.id == current_user.id:

		if 'return_on_asset' in payload:
			screen_to_update.return_on_asset = payload['return_on_asset']
		if 'cash_flow_from_operations' in payload:
			screen_to_update.cash_flow_from_operations = payload['cash_flow_from_operations']
		if 'direction_of_return_on_assets' in payload:
			screen_to_update.direction_of_return_on_assets = payload['direction_of_return_on_assets']
		if 'accrual_accounting_check' in payload:
			screen_to_update.accrual_accounting_check = payload['accrual_accounting_check']
		if 'direction_of_leverage' in payload:
			screen_to_update.direction_of_leverage = payload['direction_of_leverage']
		if 'direction_of_liquidity' in payload:
			screen_to_update.direction_of_liquidity = payload['direction_of_liquidity']
		if 'issue_stock' in payload:
			screen_to_update.issue_stock = payload['issue_stock']
		if 'direction_of_margin' in payload:
			screen_to_update.direction_of_margin = payload['direction_of_margin']
		if 'direction_of_asset_turnover' in payload:
			screen_to_update.direction_of_asset_turnover = payload['direction_of_asset_turnover']

		screen_to_update.save()
		updated_screen_dict = model_to_dict(screen_to_update)
		updated_screen_dict['poster'].pop('password')

		return jsonify(
			data=updated_screen_dict,
			message=f"Successfully updated your screen with id {id}",
			status=200
		), 200

	else:
		return jsonify(
			data={
				'error': '403 Forbidden'
			},
			message="Username does not match screen id. Only OP can update",
			status=403
		), 403

# show screens - GET /<id>/
@screens.route('/<id>', methods=['GET'])
def show_screen(id):

	screen = models.Screen.get_by_id(id)

	if not current_user.is_authenticated:
		return jsonify(
			data={
				'return_on_asset': screen.return_on_asset,
				'cash_flow_from_operations': screen.cash_flow_from_operations,
				'direction_of_return_on_assets': screen.direction_of_return_on_assets,
				'accrual_accounting_check': screen.accrual_accounting_check,
				'direction_of_leverage': screen.direction_of_leverage,
				'direction_of_liquidity': screen.direction_of_liquidity,
				'issue_stock': screen.issue_stock,
				'direction_of_margin': screen.direction_of_margin,
				'direction_of_asset_turnover': screen.direction_of_asset_turnover
			},
			message="Registered users can see the info about this screening",
			status=200
		), 200

	else:
		screen_dict = model_to_dict(screen)
		screen_dict['poster'].pop(password)

		if screen.poster.id != current_user.id:
			screen_dict.pop('date_posted')

		return jsonify(
			data=screen_dict,
			message=f"Found screen with id {id}",
			status=200
		), 200

# destroy screen - DELETE /<id>/
@screens.route('/<id>', methods=['DELETE'])
@login_required
def delete_screen():

	try:

		screen_to_delete = models.Screen.get_by_id(id)

		if screen_to_delete.poster.id == current_user.id:
			screen_to_delete.delete_instance()

			return jsonify(
				data={},
				message=f"Successfully deleted screen with id {id}",
				status=200
			), 200

		else:

			return jsonify(
				data={
					'error': '403 Forbidden'
				},
				message="Username does not match screen id. Only OP can delete",
				status=403
			), 403

	except models.DoesNotExist:
		return jsonify(
			data={
				'error': '404 Not Found'
			},
			message="Sorry, but there is no record of a screen that ID here",
			status=404
		), 404





