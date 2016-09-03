'''
__author__ = 'anis'
Date: 26.08.16
Time: 23:29
'''
import uuid
import re

from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors


class Store(object):

    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        # Sample Constructor
        # Store("John Lewis", "http://www.johnlewis.com", "span", {"itemprop": "price", "class": "now-price"})

        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def save_to_db(self):
        Database.insert(StoreConstants.COLLECTION, self.json())

    def update_db(self, store_id):
        Database.update(StoreConstants.COLLECTION, {"_id": store_id}, self.json())

    def delete_from_db(self):
        Database.remove(StoreConstants.COLLECTION, {"_id": self._id})

    def json(self):
        return {
            "name": self.name,  # store name
            "url_prefix": self.url_prefix,  # store url prefix
            "tag_name": self.tag_name,  # item's tag
            "query": self.query,  # item's query
            "_id": self._id  # store id
        }

    @classmethod
    def find_by_id(cls, store_id):
        store_obj = Database.find_one(StoreConstants.COLLECTION, {"_id": store_id})
        return cls(**store_obj)

    @classmethod
    def find_by_name(cls, store_name):
        store_obj = Database.find_one(StoreConstants.COLLECTION, {"name": store_name})
        return cls(**store_obj)

    @classmethod
    def find_by_url_prefix(cls, url_prefix):
        store_obj = Database.find_one(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}})
        return cls(**store_obj)

    @classmethod
    def find_by_url(cls, url):
        """
        Return a store from a url like "http://www.johnlewis.com/house-by-john-lewis-curve-dining-chair-white/p231441579"
        http://www.johnlewis.com --> is the prefix stored in the Store, thus call the find_by_url_prefix to get Store
        :param url: The item's URL
        :return: a Store, or raises a StoreNotFoundException if no store matches the url
        """
        store_obj = Database.find(StoreConstants.COLLECTION, {})
        url_list = [store['url_prefix'] for store in store_obj]
        url_matcher = re.compile(r"https?://(www\.)?")
        for index in range(len(url_list)):
            store_url = url_matcher.sub('', url_list[index].strip())
            if store_url in url:
                return Store.find_by_url_prefix(url_list[index])
        raise StoreErrors.StoreNotFoundError("The URL Prefix used to find store didn't result anything.")

    @classmethod
    def get_all_stores(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]
