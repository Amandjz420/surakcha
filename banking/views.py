from rest_framework.permissions import AllowAny, IsAuthenticated

from elapi.base_views import CreateView
from elapi.exceptions import InvalidDataException, APIOValidationException
from .schema import PublicTokenApiSchema
from .helper import get_access_token, get_account_item_details
from .models import Item


class AccessTokenExchange(CreateView):

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
