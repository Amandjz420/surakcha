import requests
import json

from datetime import datetime, timedelta
from celery import task
from django.conf import settings

from .models import Item, Product, Transaction,\
    TransactionCategory, Account


def get_access_token(public_token):
    data = settings.PLAID_FORMDATA.copy()
    data['public_token'] = public_token
    headers = {'Content-type': 'application/json'}
    url = settings.PLAID_URL + '/item/public_token/exchange'
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        return json.loads(resp.text)


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
        item.recent_tried = item.recent_tried + 1
        item.save()


def process_transactions(data, item):
    user = item.user
    accounts = handle_accounts(data['accounts'], user, item)
    handle_transaction(data['transactions'], accounts)
    handle_item(data['item'])


def handle_transaction(transactions, accounts):
    for transaction in transactions:
        acc_obj = accounts[transaction['account_id']]
        if transaction['transaction_id']:
            transaction_obj, created = Transaction.objects.get_or_create(
                transaction_id=transaction['transaction_id'],
                defaults={
                    'amount': transaction['amount'],
                    'authorized_date': transaction['authorized_date'],
                    'date': transaction['date'],
                    'account_id': acc_obj.id,
                    'pending_transaction_id': transaction['pending_transaction_id'],
                    'transaction_type': transaction['transaction_type'],
                    'currency': transaction['iso_currency_code'],
                    'pending': transaction['pending'],
                    'name': transaction['name']
                }
            )
        else:
            transaction_obj, created = Transaction.objects.get_or_create(
                pending_transaction_id=transaction['pending_transaction_id'],
                defaults={
                    'amount': transaction['amount'],
                    'authorized_date': transaction['authorized_date'],
                    'date': transaction['date'],
                    'account_id': acc_obj.id,
                    'transaction_id': transaction['transaction_id'],
                    'transaction_type': transaction['transaction_type'],
                    'currency': transaction['iso_currency_code'],
                    'pending': transaction['pending'],
                    'name': transaction['name']
                }
            )

        categories = []
        for cat in transaction['category']:
            category, created = TransactionCategory.objects.get_or_create(name=cat)
            categories.append(category)
        for obj in categories:
            transaction_obj.category.add(obj)
        transaction_obj.save()


def handle_accounts(accounts, user, item):
    acc = {}
    for account in accounts:
        if account['account_id'] in acc:
            account_obj, created = acc[account['account_id']], False
        else:
            account_obj, created = Account.objects.get_or_create(
                account_id=account['account_id'],
                defaults={
                    'currency': account['balances']['iso_currency_code'],
                    'available_balance': account['balances']['available'] or 0,
                    'current_balance': account['balances']['current'] or 0,
                    'official_name': account['official_name'],
                    'subtype': account['subtype'],
                    'type': account['type'],
                    'user_id': user.id,
                    'item_id': item.id,
                }
            )
            acc[account['account_id']] = account_obj
        if not created:
            account_obj.currency = account['balances']['iso_currency_code']
            account_obj.available = account['balances']['available']
            account_obj.current = account['balances']['current']
            account_obj.official_name = account['official_name']
            account_obj.save()
    return acc


def handle_item(item):
    available_products = []
    for product in item['available_products']:
        obj, created = Product.objects.get_or_create(name=product)
        available_products.append(obj)

    billed_products = []
    for product in item['billed_products']:
        obj, created = Product.objects.get_or_create(name=product)
        billed_products.append(obj)

    item_obj = Item.objects.get(item_id=item['item_id'])
    for bill_product in billed_products:
        item_obj.billed_product.add(bill_product)
    for av_product in available_products:
        item_obj.avail_product.add(av_product)
    item_obj.institution_id = item['institution_id']
    item_obj.updated = True
    item_obj.recent_tried = 0
    item_obj.save()