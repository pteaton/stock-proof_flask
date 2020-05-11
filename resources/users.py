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
	payload = request.get_json()

	payload['email'] = payload['email'].lower()
	payload['username'] = payload['username'].lower()
	print(payload)

	try:
		models.User.get(models.User.email == payload['email'])

		return jsonify(
			data={},
			message=f"Sorry bud, a user with the email {payload['email']} already exists",
			status=401
		), 401

	except models.DoesNotExist:
		pw_hash = generate_password_hash(payload['password'])

		created_user = models.User.create(
			username=payload['username'],
			email=payload['email'],
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