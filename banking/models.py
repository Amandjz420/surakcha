from django.db import models
from encrypted_fields import fields

from authn.models import User


class Product(models.Model):

    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0}".format(self.name)

    def __str__(self):
        return "{0}".format(self.name)


class TransactionCategory(models.Model):

    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'transactioncategories'

    def __unicode__(self):
        return "{0}".format(self.name)

    def __str__(self):
        return "{0}".format(self.name)


class Item(models.Model):

    item_id = models.CharField(max_length=200, blank=True, null=True)
    access_token = fields.EncryptedCharField(max_length=200, editable=False)
    user = models.ForeignKey(User, related_name='item_user', blank=True, null=True, on_delete=models.SET_NULL)
    institution_id = models.CharField(max_length=100, blank=True, null=True)
    avail_product = models.ManyToManyField(Product, related_name='item_avail', blank=True, null=True)
    billed_product = models.ManyToManyField(Product, related_name='item_billed', blank=True, null=True)
    updated = models.BooleanField(default=False)
    recent_tried = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0}, {1}".format(self.institution_id, self.user.username)

    def __str__(self):
        return "{0}, {1}".format(self.institution_id, self.user.username)


# class AccountType(models.Model):
#
#     name = models.CharField(max_length=100, blank=True, null=True)
#     parent_type = models.ForeignKey('AccountType', blank=True, null=True, on_delete=models.SET_NULL)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified = models.DateTimeField(auto_now=True)
#
#     def __unicode__(self):
#         return "{0}".format(self.name)
#
#     def __str__(self):
#         return "{0}".format(self.name)


class Account(models.Model):

    account_id = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='accounts_user', blank=True, null=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='accounts_item', blank=True, null=True, on_delete=models.SET_NULL)
    current_balance = models.FloatField(default=0)
    currency = models.CharField(max_length=20, blank=True, null=True)
    available_balance = models.FloatField(default=0)
    official_name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    subtype = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0}-{1}".format(self.user.username, self.account_id)

    def __str__(self):
        return "{0}-{1}".format(self.user.username, self.account_id)


class Transaction(models.Model):

    name = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=200)
    pending_transaction_id = models.CharField(max_length=200, blank=True, null=True)
    transaction_type = models.CharField(max_length=50, blank=True, null=True)
    account = models.ForeignKey(Account, related_name='transaction_account', blank=True, null=True, on_delete=models.SET_NULL)
    amount = models.FloatField()
    currency = models.CharField(max_length=20)
    date = models.DateField()
    pending = models.BooleanField(default=False)
    authorized_date = models.DateField(blank=True, null=True)
    category = models.ManyToManyField(TransactionCategory, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0}-{1}".format(self.name, self.transaction_id)

    def __str__(self):
        return "{0}-{1}".format(self.name, self.transaction_id)

