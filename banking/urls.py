from django.conf.urls import url

from . import views

app_name = 'banking'
urlpatterns = [
    url(r'^token_exchange/$', views.AccessTokenExchangeApi.as_view(), name='access_token'),
    url(r'^transactions/update$', views.WebHookPlaidApi.as_view(), name='update_transactions'),
    url(r'^account_statement/$', views.GetAccountsDetailsApi.as_view(), name='get_details'),
]