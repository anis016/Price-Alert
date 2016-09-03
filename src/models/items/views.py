'''
__author__ = 'anis'
Date: 26.08.16
Time: 23:29
'''

from flask import Blueprint

item_blueprint = Blueprint("items", __name__)


@item_blueprint.route('/item/<string:name>')
def item_page():
    pass


@item_blueprint.route('/item/load')
def load_item():
    """
    Loads an item's data using their store and return a JSON representation of it
    :return:
    """
    pass