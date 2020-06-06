from celery import task
from .models import Item
from .helper import get_account_item_details
from datetime import datetime


@task(name='transactions_update')
def check_details_update():
    not_updated_item = Item.objects.filter(updated=False, recent_tried__lt=3)
    for item in not_updated_item:
        get_account_item_details.delay(item.item_id)