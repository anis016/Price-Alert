'''
__author__ = 'anis'
Date: 26.08.16
Time: 23:29
'''
import uuid

import requests
from bs4 import BeautifulSoup
import re

from src.common.database import Database
import src.models.items.constants as ItemConstants
from src.models.stores.store import Store


class Item(object):

    def __init__(self, name, url, price=None, _id=None):
        # Sample Constructor
        # Item("John Lewis Curve Dining Chair, White",
        #     "http://www.johnlewis.com/house-by-john-lewis-curve-dining-chair-white/p231441579",
        #     Store("John Lewis", "http://www.johnlewis.com", "span", {"itemprop": "price", "class": "now-price"}))

        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self._id = uuid.uuid4().hex if _id is None else _id
        self.price = None if price is None else price

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        """
        Load the price of a particular item from the store with the tag_name and query supplied
        :param tag_name: HTML tag name eg: span, p, etc
        :param query: dictionary which takes input the identifier such as id, class etc
        :return:
        """
        # Amazon: <span id="priceblock_ourprice" class="a-size-medium a-color-price">EUR 69.99</span>

        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile('(\d+.\d+)')
        match = pattern.search(string_price)

        self.price = float(match.group())
        return self.price

    def save_to_db(self):
        Database.insert(ItemConstants.COLLECTION, self.json())

    def update_db(self):
        Database.update(ItemConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "name": self.name,
            "url": self.url,
            "_id": self._id,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))
