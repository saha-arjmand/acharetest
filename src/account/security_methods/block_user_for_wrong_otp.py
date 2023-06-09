
from pathlib import Path
import datetime
import sys
# solved python search path for import module in other sub directories
original_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(original_path)
from .. import models

"""
    Block the user in case of wrong otp login
"""
def check_block_user(id):

    otp_user = models.OtpCode.objects.get(account = id)
    if otp_user.wrong_code_enter_by_time == 3:

        now = datetime.datetime.now()
        block_time = otp_user.block_time
        diff_time = now - block_time

        if diff_time.seconds >= 60 * 60:
            otp_user.user_block = False
            otp_user.wrong_code_enter_by_time = 0
            otp_user.save()
            print("You are unblocked !")
            return False
        else:
            print(f"Remaining time to unblock is {(3600 - diff_time.seconds)//60} minutes")
            return True

    elif otp_user.wrong_code_enter_by_time < 3:
        return False

    

def wrong_otp(id):
    try:
        otp_user = models.OtpCode.objects.get(account = id)

        if otp_user.wrong_code_enter_by_time < 3:
            otp_user.wrong_code_enter_by_time += 1
            otp_user.save()

            if otp_user.wrong_code_enter_by_time == 3:
                otp_user.user_block = True

                # set block time
                now = datetime.datetime.now()
                otp_user.block_time = now

                otp_user.save()
                print("Your user has been blocked due to entering the wrong otp !")

        elif otp_user.wrong_code_enter_by_time > 3:
            otp_user.wrong_code_enter_by_time = 3
            otp_user.save()

        print(f"this is number of wrong time : {otp_user.wrong_code_enter_by_time}")

    except models.Account.DoesNotExist:
        return False