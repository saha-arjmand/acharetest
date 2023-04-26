
import datetime
from pathlib import Path
import sys
# solved python search path for import module in other sub directories
original_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(original_path)
from .. import models

"""
    Wait if user enter the wrong code
"""
def wait_sms(mobile):
    account_exist = models.Account.objects.filter(phone_number=mobile).exists()

    if account_exist:
        id = models.Account.objects.get(phone_number = mobile)
        otp_exist = models.OtpCode.objects.filter(account = id).exists()

        if otp_exist == False:
            return True
        else:
            try:
                otp_user = models.OtpCode.objects.get(account = id)
                now = datetime.datetime.now()
                otp_time = otp_user.otp_create_time
                diff_time = now - otp_time

                if diff_time.seconds > 10:
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
    

