from random import randint
from . import models
import datetime
from kavenegar import *
from mysite.settings import Kavenegar_API

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