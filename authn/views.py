from rest_framework.permissions import AllowAny, IsAuthenticated

from elapi.base_views import CreateView
from .schema import LoginSchema, OTPSchema
from .models import LoginOtpLog, User
from .authn_helper import get_date_difference_in_minutes, send_sms_otp


class Login(CreateView):

    schema_class = LoginSchema
    permission_classes = (AllowAny,)
    post_status_code = 201

    def perform_create(self, data):
        existing_user = data['existing_user']
        otp = LoginOtpLog.objects.filter(mobile=data['mobile']).last()
        if otp and get_date_difference_in_minutes(otp.created_at) < 15:
            send_sms_otp(data['mobile'], data['name'], otp.otp)
            self.post_status_code = 200
        else:
            LoginOtpLog.objects.create(
                mobile=data['mobile'],
                otp=data['otp'],
                name=data['name'])
            send_sms_otp(data['mobile'], data['name'], data['otp'])
        return {'success': "OTP has been sent", 'existing_user': existing_user}


class VerifyOtp(CreateView):

    schema_class = OTPSchema
    permission_classes = (AllowAny,)
    post_status_code = 200

    def perform_create(self, data):
        otp = LoginOtpLog.objects.filter(mobile=data['mobile'], otp=data['otp']).last()
        if otp and get_date_difference_in_minutes(otp.created_at) < 15 and not otp.used:
            if User.objects.filter(mobile=otp.mobile).exists():
                user = User.objects.get(mobile=otp.mobile)
            else:
                email = data['email']
                gender = data['gender'] or None
                user = User.objects.create_user(
                    mobile=otp.mobile,
                    username=otp.name,
                    email=email,
                    gender=gender
                )
            otp.used = True
            otp.save()
            return {
                'token': user.token,
                'id': user.id
            }
        return {'failed': "login again"}
