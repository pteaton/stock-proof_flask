# imports
import models
from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user, login_required

# Blueprint
users = Blueprint('users', 'users')

# user route test
@users.route('/', methods=['GET'])
def text_user_resource():
	return "user resource working"

# register user
@users.route('/register', methods=['POST'])
def register():
	print("here please work")
	payload = request.get_json()
	print("ABOVE THIS IS THE PAYLOAD\n\n\n\n")
	payload['username'] = payload['username'].lower()
	payload['email'] = payload['email'].lower()
	# need this? payload['bio'] = payload['bio'].lower()
	print(payload)

	try:

		models.User.get(models.User.username == payload['username'])

		return jsonify (
			data = {},
			message = "Sorry that username is already taken",
			status = 401
		), 401

	except models.DoesNotExist:

		try: 
			models.User.get(models.User.email == payload['email'])

			return jsonify(
				data={},
				message=f"Sorry but a user with the email {payload['email']} already exists",
				status=401
			), 401

		except models.DoesNotExist:
			pw_hash = generate_password_hash(payload['password'])

			created_user = models.User.create(
				username=payload['username'],
				email=payload['email'],
				bio=payload['bio'],
				password=pw_hash
			)
			print(created_user)

			login_user(created_user)

			created_user_dict = model_to_dict(created_user)
			print(created_user_dict)

			print(type(created_user_dict['password']))

			created_user_dict.pop('password')

			return jsonify(
				data=created_user_dict,
				message=f"Successfully registered user {created_user_dict['email']}",
				status=201
			), 201
# login
@users.route('/login', methods=['POST'])
def login():

	payload = request.get_json()
	payload['username'] = payload['username'].lower()
	print("Login route, here's payload, does this work?", payload)

	# look up username to help?
	try:
		user = models.User.get(models.User.username == payload['username'])
		

		user_dict = model_to_dict(user)
		print("WORKING? working?", user_dict)
		good_password = check_password_hash(user_dict['password'], payload['password'])

		if good_password:

			login_user(user)

			user_dict.pop('password')
			
			return jsonify(
				data = user_dict,
				message = f'Hey {user_dict["username"]}!',
				status = 201
			), 201

		else:

			print("bad password")

			return jsonify(
				data = {},
				message = "Wrong username or password :(",
				status = 401
			), 401

	except models.DoesNotExist:

		print("bad username")

		return jsonify(
			data = {},
			message = "Wrong username or password :(",
			status = 401
		), 401

# user show route
@users.route('/<id>', methods=['GET'])
def show_user(id):
	user = models.User.get(models.User.id == id)
	user_dict = model_to_dict(user)
	user_dict.pop('password')

	print(user_dict)
	user_stocks = [model_to_dict(stocks) for stocks in user.stocks]
	print('user_stock', user_stock)

	return jsonify(
		data = user_dict,
		artworks=user_stock,
		message = f'Display info for {user_dict["username"]}, ID#{user_dict["id"]}',
		status = 200
	), 200

# destroy user
@users.route('/<id>', methods=['DELETE'])
@login_required
def delete_account(id):
	user_to_delete = models.User.get_by_id(id)

	if current_user.id == user_to_delete.id:
		user_to_delete.delete_instance()

		return jsonify(
			data={},
			message="Your account has been successfully deleted",
			status=200
		), 200

	else:
		return jsonify(
			data={},
			message="This account does not belong to you",
			status=403
		), 403

	return "delete route here"

# edit user
@users.route('/<id>', methods=['PUT'])
@login_required
def edit_user(id):
	payload = request.get_json()
	user_to_edit = models.User.get_by_id(id)

	if current_user.id == user_to_edit.id:

		user_to_edit.username = payload['username']
		user_to_edit.email = payload['email']
		user_to_edit.bio = payload['bio']

		user_to_edit.save()

		user_to_edit_dict = model_to_dict(user_to_edit)

		return jsonify(
			data = user_to_edit_dict,
			message = 'Successfully edited your profile',
			status = 201
		), 201

	else:

		return jsonify(
			data = {},
			message = "That is not your account",
			status = 403
		), 403



# logout user
@users.route('/logout', methods=['GET'])
def logout():
	logout_user()
	return jsonify(
		data={},
		message="Successfully logged out.",
		status=200
	), 200


