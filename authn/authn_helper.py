import datetime
import re
import time
import pytz
import requests

from random import randrange
from django.utils import timezone
from celery import shared_task
from django.conf import settings

MIN_OTP_VALUE = 100000
MAX_OTP_VALUE = 999999


def valid_mobile_number(mobile):
    return re.findall(r'^[6789]\d{9}', str(mobile))


def get_date_difference_in_minutes(datetimestamp):
    # Convert to Unix timestamp
    d1_ts = time.mktime(datetimestamp.timetuple())
    d2_ts = time.mktime(timezone.now().timetuple())
    return int(d2_ts - d1_ts) / 60


def get_timezone_aware_current_datetime():
    return datetime.now(pytz.timezone('Asia/Kolkata'))


def create_otp(otp=None):
    if not otp:
        otp = randrange(MIN_OTP_VALUE, MAX_OTP_VALUE + 1)
    return otp


@shared_task
def send_sms_otp(mobile, name, otp):
    # logic for sending sms
    pass