from django.contrib import admin

from .models import Transaction, TransactionCategory, Account,\
    Product, Item


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Transaction._meta.fields]


# @admin.register(AccountType)
# class AccountTypeAdmin(admin.ModelAdmin):
#     list_display = [f.name for f in AccountType._meta.fields]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Item._meta.fields]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Product._meta.fields]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Account._meta.fields]


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TransactionCategory._meta.fields]

