'''
__author__ = 'anis'
Date: 26.08.16
Time: 22:46
'''

from src.app import app

app.run(debug=app.config['DEBUG'])
