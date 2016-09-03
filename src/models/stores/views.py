'''
__author__ = 'anis'
Date: 26.08.16
Time: 23:29
'''

from flask import Blueprint
from flask import json
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.utils import redirect

from src.models.stores.store import Store
import src.common.decorators as decorators

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
def index():
    stores = Store.get_all_stores()
    return render_template('stores/list_store.html', stores=stores)


@store_blueprint.route('/<string:store_id>')
def store_page(store_id):
    store = Store.find_by_id(store_id)
    return render_template('stores/store.html', store=store)


@store_blueprint.route('/new', methods=['POST', 'GET'])
@decorators.requires_admin_permission
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        store = Store(name, url_prefix, tag_name, query)
        store.save_to_db()

        return redirect(url_for('stores.index'))

    return render_template('stores/create_store.html')


@store_blueprint.route('/edit/<string:store_id>', methods=['POST', 'GET'])
@decorators.requires_admin_permission
def edit_store(store_id):
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        store = Store(name, url_prefix, tag_name, query, store_id)
        store.update_db(store_id)

        return redirect(url_for('stores.index'))

    store = Store.find_by_id(store_id)
    return render_template('stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@decorators.requires_admin_permission
def delete_store(store_id):
    Store.find_by_id(store_id).delete_from_db()
    return redirect(url_for('stores.index'))
