import os
from flask import Flask, jsonify, g
import models
from resources.users import users
from resources.stocks import stocks
from flask_login import LoginManager
from flask_cors import CORS

DEBUG=True
PORT=8000

app = Flask(__name__)

# Login Authentication
app.secret_key = "This is a secret."
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	try:
		print("loading the following user")
		user = models.User.get_by_id(user_id)

		return user

	except models.DoesNotExist:
		return None

@login_manager.unauthorized_handler
def unauthorized():
	return jsonify(
		data={
		'Error': 'User is not logged in'
		},
		message="You must be logged in to access this resource.",
		status=401
	), 401

# CORS
CORS(stocks, origins=['http://localhost:3000'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)


# Blueprint
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(stocks, url_prefix='/api/v1/stocks')

# jsonify test
@app.route('/test_json')
def get_json():
	return jsonify(['that', 'this', 'and the other'])




# Run App
if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)