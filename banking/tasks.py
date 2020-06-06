import logging
import json
import requests

from celery import task
from datetime import datetime, timedelta
from django.conf import settings

from .models import Item
from .helper import process_transactions

logger = logging.getLogger(__name__)


@task(name='transactions_update')
def check_details_update():
    not_updated_item = Item.objects.filter(updated=False, recent_tried__lt=3)
    for item in not_updated_item:
        get_account_item_details.delay(item.item_id)


@task(name='get_updated_details')
def get_account_item_details(item_id):
    item = Item.objects.get(item_id=item_id)
    data = settings.PLAID_FORMDATA.copy()
    data['access_token'] = item.access_token
    date_today = datetime.now()
    date_before_2_yrs = date_today - timedelta(days=730)
    data['start_date'] = date_before_2_yrs.strftime('%Y-%m-%d')
    data['end_date'] = date_today.strftime('%Y-%m-%d')
    headers = {'Content-type': 'application/json'}
    url = settings.PLAID_URL + '/transactions/get'
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    if resp.status_code == 200:
         process_transactions(resp.json(), item)
    else:
        logger.error("Couldn't update the transactions because: \n " + str(resp.text))
        item.recent_tried = item.recent_tried + 1
        item.save()
