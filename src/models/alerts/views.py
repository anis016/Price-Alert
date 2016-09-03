'''
__author__ = 'anis'
Date: 26.08.16
Time: 23:29
'''

from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.common.decorators as decorators

alert_blueprint = Blueprint("alerts", __name__)  # first parameter is the url prefix www.mysite.com/alerts/api


@alert_blueprint.route('/')
def index():
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@decorators.requires_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = float(request.form['price_limit'])

        item = Item(name, url)
        item.save_to_db()

        alert = Alert(session['email'], price_limit, item._id)
        alert.update_item_price()  # This also saves the alert alongside

        return redirect(url_for('users.user_alerts'))

    return render_template('alerts/create_alert.html')


@alert_blueprint.route('/deactivate/<string:alert_id>')
@decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
@decorators.requires_login
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/delete/<string:alert_id>')
@decorators.requires_login
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).delete_from_db()
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/<string:alert_id>')
@decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/alert.html', alert=alert)


@alert_blueprint.route('/check_price/<string:alert_id>')
@decorators.requires_login
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).update_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))


@alert_blueprint.route('/edit/<string:alert_id>', methods=['POST', 'GET'])
@decorators.requires_login
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)

    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit

        alert.update_db()
        return redirect(url_for('alerts.index'))

    return render_template('alerts/edit_alert.html', alert=alert)