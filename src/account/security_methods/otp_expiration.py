
import datetime
from pathlib import Path
import sys
# solved python search path for import module in other sub directories
original_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(original_path)
from .. import models

"""
    Expiration time of sent SMS
"""
def check_otp_expiration(id):

    try:
        otp_user = models.OtpCode.objects.get(account = id)
        now = datetime.datetime.now()
        otp_time = otp_user.otp_create_time
        diff_time = now - otp_time

        expiration_time = 120 - int(diff_time.seconds)
        if expiration_time > 0:
            print(f"Remaining time until expiration:e : {expiration_time}")

        if diff_time.seconds > 120:
            print("OTP has expired")
            return False
        else:
            print("OTP has not expired")
            return True
        
    except models.Account.DoesNotExist:
        return False