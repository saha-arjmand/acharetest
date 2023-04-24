from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    
    def create_user(self, phone_number, email, first_name, last_name ,password=None):
        if not phone_number:
            raise ValueError("Users must have a phoneNumber")
        if not email:
            raise ValueError("Users must have an email")
        if not first_name:
            raise ValueError("User must have a firstName")
        if not last_name:
            raise ValueError("User must have a lastName")

        user = self.model(
            phone_number = phone_number,
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, first_name, last_name ,password):
        user = self.create_user(
            phone_number = phone_number,
            password = password,
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    username                = None
    phone_number            = models.CharField(max_length=11, unique=True)
    email                   = models.EmailField(verbose_name="email", max_length=60)
    first_name              = models.CharField(max_length=30)
    last_name               = models.CharField(max_length=30)
    ip                      = models.CharField(max_length=50, blank=True, null=True)

    date_joined             = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name="last login", auto_now=True)

    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    

    # This code tell Django which field to login with
    USERNAME_FIELD = 'phone_number'
    # These fields are necessary for the register
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name',]

    # Set Manager
    objects = MyAccountManager()

    # backend = ''

    def __str__(self) :
        return self.first_name + " " + self.last_name + " , " + str(self.phone_number)

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class OtpCode(models.Model):
    phone_number                        = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    otp                                 = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time                     = models.DateTimeField(auto_now=True)
    wrong_code_enter_by_time            = models.PositiveIntegerField(default=0)
    time_of_wrong_code_enter_by_time    = models.DateTimeField(auto_now=True)
    user_block                          = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number