from django.conf.urls import url

from . import views

app_name = 'authn'
urlpatterns = [
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'resend_otp/$', views.Resend.as_view(),  name='resend'),
    url(r'verify_otp/$',  views.VerifyOtp.as_view(), name='verifyOtp'),
]