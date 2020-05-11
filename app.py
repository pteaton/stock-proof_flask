from flask import Flask
from resources.users import users
from resources.stocks import stocks
import models
from flask_login import LoginManager

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
		'error': 'User is not logged in'
		},
		message="You must be logged in to access this resource.",
		status=401
	), 401


# Blueprint
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(stocks, url_prefix='/api/v1/stocks')

# jsonify test
@app.route('/test_json')
def get_json():
	return jsonify(['that', 'this', 'and the other'])




# Run App
if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT)

