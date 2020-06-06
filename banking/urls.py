from django.conf.urls import url

from . import views

app_name = 'banking'
urlpatterns = [
    url(r'^token_exchange/$', views.AccessTokenExchange.as_view(), name='accessToken'),
    # url(r'resend_otp/$', views.Login.as_view(),  name='resend'),
    # url(r'verify_otp/$',  views.VerifyOtp.as_view(), name='verifyOtp'),
]