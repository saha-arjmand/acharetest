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
        print(f"expiration time : {diff_time.seconds}")

        if diff_time.seconds > 120:
            return False
        else:
            return True
        
    except models.Account.DoesNotExist:
        return False
    

"""
    Wait if user enter the wrong code
"""
def wait_sms(mobile):
    account_exist = models.Account.objects.filter(phone_number=mobile).exists()
    if account_exist:
        id = models.Account.objects.get(phone_number = mobile)

        try:
            otp_user = models.OtpCode.objects.get(account = id)
            now = datetime.datetime.now()
            otp_time = otp_user.otp_create_time
            diff_time = now - otp_time

            if diff_time.seconds > 120:
                # update send code time
                models.OtpCode.objects.filter(account = id).update(otp_create_time=datetime.datetime.now())
                return True
            else:
                print("The user must wait")
                print(f"wait for : {120 - diff_time.seconds} seconds")
                return False
            
        except models.Account.DoesNotExist:
            return False
    else:
        return True
    

def block_wrong_password_check(mobile, wrong = False):
    # check user not block
    # This function is executed when the user enters the wrong password
    try:
        otp_user = models.OtpCode.objects.get(phone_number = mobile)
        # add one to wrong code entered
        if wrong == True:
            otp_user.wrong_code_enter_by_time = int(otp_user.wrong_code_enter_by_time) + 1
            otp_user.save()

        if otp_user.wrong_code_enter_by_time == 3:
            user = "block"


        if user == "block":
            return True
        else:
            now = datetime.datetime.now()
            block_time = otp_user.time_of_wrong_code_enter_by_time
            diff_time = now - block_time
            if diff_time.seconds <= 3600:
                print(f"Time left to get out of the block : {(3600 - diff_time.seconds)/ 60} mins")
            return False

        # # check user is block ?
        # if otp_user.wrong_code_enter_by_time == 3 :
        #     # update block time
        #     otp_user.time_of_wrong_code_enter_by_time = datetime.datetime.now()
        #     otp_user.save()
        #     print("blocki amoo")
        #     return True

        # else :
        #     if otp_user.user_block == True:
        #         now = datetime.datetime.now()
        #         block_time = otp_user.time_of_wrong_code_enter_by_time
        #         diff_time = now - block_time
        #         if diff_time.seconds <= 3600:
        #             print(f"Time left to get out of the block : {(3600 - diff_time.seconds)/ 60} mins")
        #             return False
        #         else:
        #             otp_user.user_block = False
        #             otp_user.save()
        #             print("The user is unblocked")
        #             return False
            

    except models.Account.DoesNotExist:
        return False