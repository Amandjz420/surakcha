from rest_framework.permissions import AllowAny, IsAuthenticated

from elapi.base_views import CreateView, ListView
from elapi.exceptions import InvalidDataException, APIOValidationException
from .schema import PublicTokenApiSchema, WebHookPlaidApiSchema, AccountSchema
from .helper import get_access_token, get_account_item_details
from .models import Item, Account


class AccessTokenExchangeApi(CreateView):

    schema_class = PublicTokenApiSchema
    permission_classes = (IsAuthenticated,)
    post_status_code = 200

    def perform_create(self, data):
        resp_data = get_access_token(data['public_token'])
        if 'error_code' in resp_data:
            self.throw_error({
                'error_message': resp_data['error_message'],
                'error_code': resp_data['error_code']
            })
        item_id = resp_data['item_id']
        access_token = resp_data['access_token']
        item, created = Item.objects.get_or_create(
            item_id=item_id,
            defaults={
                'access_token': access_token,
                'user_id': self.request.user.id
            }
        )
        get_account_item_details(item, self.request.user)
        return {'success': True, 'item_id': item_id}


class WebHookPlaidApi(CreateView):

    schema_class = WebHookPlaidApiSchema
    permission_classes = (AllowAny,)
    post_status_code = 200

    def perform_create(self, data):
        item = data.pop('item')
        item.updated = False
        item.recent_tried = 0
        item.save()
        if 'new_transactions' in data and data['new_transactions'] > 0:
            get_account_item_details(item, self.request.user)
        return {'message': 'Recieved', 'code': 'TRANSACTION_UPDATE'}


class GetAccountsDetailsApi(ListView):

    schema_class = AccountSchema
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query = Account.objects.\
            prefetch_related('transaction_account', 'transaction_account__category').filter(user=self.request.user)
        if self.request.GET.get('account_id', None):
            query = query.filter(account_id=self.request.GET['account_id'])
        return query