from marshmallow import post_load, validates

from elapi.base_schema import Schema
from elapi.fields import fields
from elapi.exceptions import InvalidDataException

from .models import Item


class PublicTokenApiSchema(Schema):
    """
    User API Schema
    """
    public_token = fields.String(required=True)


class WebHookPlaidApiSchema(Schema):
    """
    Webhook api for plaid Schema
    """
    webhook_code = fields.String()
    webhook_type = fields.String()
    item_id = fields.String()
    error = fields.String(allow_none=True)
    new_transaction = fields.String()

    @post_load
    def get_item_obj(self, data):
        data['item'] = Item.objects.get(item_id=data['item_id'])
        return data


class TransactionSchema(Schema):
    """
    Account Schema
    category = models.ManyToManyField(TransactionCategory, blank=True, null=True)

    """
    name = fields.String()
    transaction_id = fields.String()
    pending_transaction_id = fields.String()
    transaction_type = fields.String()
    currency = fields.String()
    date = fields.Date()
    authorized_date = fields.Date()
    pending = fields.Boolean()
    amount = fields.Number()
    categories = fields.Method('get_categories')

    def get_categories(self, instance, **kwargs):
        categories = [x['name'] for x in list(instance.category.all().values('name'))]
        return categories


class AccountSchema(Schema):
    """
    AccountSchema
    """
    item_id = fields.String(attribute='item.item_id')
    updated = fields.String(attribute='item.updated')
    current_balance = fields.Number()
    available_balance = fields.Number()
    account_id = fields.String(required=False, allow_none=True)
    official_name = fields.String(required=False, allow_none=True)
    currency = fields.String(required=False, allow_none=True)
    type = fields.String(required=False, allow_none=True)
    subtype = fields.String(required=False, allow_none=True)
    transactions = fields.Method('get_transaction')

    def get_transaction(self, instance, **kwargs):
        return TransactionSchema().dump(instance.transaction_account.all(),many=True)