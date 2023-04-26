
from pathlib import Path
import datetime
import sys
# solved python search path for import module in other sub directories
original_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(original_path)
from .. import models

"""
    Block the user in case of wrong password login
"""
def login_check_block_user(phone_number):

    user = models.Account.objects.get(phone_number = phone_number)
    if user.number_of_wrong_password_enter == 3:

        now = datetime.datetime.now()
        block_time = user.block_time
        diff_time = now - block_time

        if diff_time.seconds >= 60 * 60:
            user.user_block = False
            user.number_of_wrong_password_enter = 0
            user.save()
            print("You are unblocked !")
            return False
        else:
            print(f"Remaining time to unblock is {(3600 - diff_time.seconds)//60} minutes")
            return True

    elif user.number_of_wrong_password_enter < 3:
        return False

    

def login_wrong_password(phone_number):
    try:
        user = models.Account.objects.get(phone_number = phone_number)

        if user.number_of_wrong_password_enter < 3:
            user.number_of_wrong_password_enter += 1
            user.save()

            if user.number_of_wrong_password_enter == 3:
                user.user_block = True

                # set block time
                now = datetime.datetime.now()
                user.block_time = now
                user.save()
                print("Your user has been blocked due to entering the wrong password !")

        elif user.number_of_wrong_password_enter > 3:
            user.number_of_wrong_password_enter = 3
            user.save()

        print(f"You have entered the wrong password for {user.number_of_wrong_password_enter}")

    except models.Account.DoesNotExist:
        return False