'''
__author__ = 'anis016'
Date: 26.08.16
Time: 23:29
'''
import uuid

import datetime
import requests

import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item
from src.config import MAILGUN_CONFIG


class Alert(object):

    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)

    def send_email(self):
        return requests.post(
            MAILGUN_CONFIG['URL'],
            auth=("api", MAILGUN_CONFIG['API_KEY']),
            data={
                "from": MAILGUN_CONFIG['FROM'],
                "to": self.user_email,
                "subject": "Price limit reached for {}".format(self.item.name),
                "text": "We have found a deal ! ({}). To navigate to the alert, visit.".format(
                    self.item.url)
            }
        )

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        """
        Check and Find all those Items that haven't been checked.
        :param minutes_since_update: Interval of checking
        :return: All the alert object's that are greater then or equal to the interval provided
        """
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      query={"last_checked": {"$lte": last_updated_limit},
                                                             "active": True})]

    def save_to_db(self):
        Database.insert(AlertConstants.COLLECTION, self.json())

    def update_db(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def delete_from_db(self):
        Database.remove(AlertConstants.COLLECTION, {"_id": self._id})

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "item_id": self.item._id,
            "user_email": self.user_email,
            'active': self.active
        }

    def update_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.update_db()
        self.update_db()
        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price < self.price_limit:
            self.send_email()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"user_email": user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {"_id": alert_id}))

    def deactivate(self):
        self.active = False
        self.update_db()

    def activate(self):
        self.active = True
        self.update_db()
