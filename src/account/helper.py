from kavenegar import *
from mysite.settings import Kavenegar_API
from random import randint
from . import models
import datetime


def sent_otp(mobile, otp):
    mobile = [mobile,]
    try:
        api = KavenegarAPI(Kavenegar_API)
        params = {
            'sender': '10008663',
            'receptor': mobile,
            'message': 'Your code is : {}'.format(otp),
        }
        response = api.sms_send(params)
        print("OTP:  ", otp)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def get_random_otp():
    return randint(1000,9999)


def check_otp_expiration(mobile):
    try:
        otp_user = models.OtpCode.objects.get(phone_number = mobile)
        now = datetime.datetime.now()
        otp_time = otp_user.otp_create_time
        diff_time = now - otp_time
        print(f"diff time : {diff_time.seconds}")

        if diff_time.seconds > 30:
            return False
        else:
            return True
        
    except models.Account.DoesNotExist:
        return False
    

def wait_sms(mobile):
    try:
        otp_user = models.OtpCode.objects.get(phone_number = mobile)
        now = datetime.datetime.now()
        otp_time = otp_user.otp_create_time
        diff_time = now - otp_time
        print(f"wait for : {120 - diff_time.seconds}")

        if diff_time.seconds > 120:
            return True
        else:
            print("The user must wait")
            return False
        
    except models.Account.DoesNotExist:
        return False