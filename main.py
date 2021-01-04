from flask import Flask, session
from flask_cors import CORS
from endpoints import menu_bp, login_bp, sign_up_bp, orders_bp, sessions_bp, notifications_bp, tables_bp, payments_bp
from datetime import timedelta
from flask_session import Session
import os


app = Flask(__name__)
CORS(app)

s = Session()

app.register_blueprint(menu_bp)
app.register_blueprint(login_bp)
app.register_blueprint(sign_up_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(sessions_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(tables_bp)
app.register_blueprint(payments_bp)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/")
def root():
	return "For api go to api/<request>"

if __name__ == "__main__":
	app.secret_key = os.urandom(24)
	app.config['SESSION_TYPE'] = 'filesystem'
	s.init_app(app)

	app.debug = True
	app.run(port=0000)
