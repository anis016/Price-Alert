'''
__author__ = 'anis016'
Date: 29.08.16
Time: 21:36
'''
from src.common.database import Database
from src.models.alerts.alert import Alert

Database.initialize()

alerts_needing_update = Alert.find_needing_update()
for alert in alerts_needing_update:
    alert.update_item_price()
    alert.send_email_if_price_reached()
