'''
__author__ = 'anis'
Date: 26.08.16
Time: 22:47
'''
import os

DEBUG = True
ADMINS = frozenset([os.environ.get('ADMIN_EMAILS')])

MAILGUN_CONFIG = {
         "URL": os.environ.get('MAILGUN_URL'),
     "API_KEY": os.environ.get('MAILGUN_API_KEY'),
        "FROM": os.environ.get('FROM')
}
