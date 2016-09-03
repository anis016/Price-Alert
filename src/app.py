'''
__author__ = 'anis'
Date: 26.08.16
Time: 22:43
'''

from flask import Flask
from flask import render_template
from flask import session

from src.common.database import Database

app = Flask(__name__)
app.config.from_object('config')  # takes the file name defined as "config". searches for the Capitalize variable to store.
app.secret_key = "1234"


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    # if session['email'] is not None:
    #     email, domain = session['email'].split('@')
    #     return render_template('home.html', email=email)
    return render_template('home.html')

from src.models.users.views import user_blueprint
from src.models.stores.views import store_blueprint
from src.models.alerts.views import alert_blueprint

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")