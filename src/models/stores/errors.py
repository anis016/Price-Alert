'''
__author__ = 'anis'
Date: 29.08.16
Time: 00:47
'''


class StoreError(Exception):

    def __init__(self, message):
        self.message = message


class StoreNotFoundError(StoreError):
    pass
