
from pathlib import Path
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
        otp_user.user_block == True
        otp_user.save()
        print("Your user has been blocked due to entering the wrong otp !")
        return True

    elif otp_user.wrong_code_enter_by_time < 3:
        return False

    

def wrong_otp(id):
    try:
        otp_user = models.OtpCode.objects.get(account = id)

        if otp_user.wrong_code_enter_by_time < 3:
            otp_user.wrong_code_enter_by_time += 1
            otp_user.save()
        elif otp_user.wrong_code_enter_by_time >= 3:
            otp_user.wrong_code_enter_by_time = 3
            otp_user.save()

        print(f"this is number of wrong time : {otp_user.wrong_code_enter_by_time}")

    except models.Account.DoesNotExist:
        return False