from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):  # Add all required fields
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        user_obj = self.model(
            email = self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.save(using = self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password = password,
        )
        user.is_staff = True
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password = password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser):
    DESIG = (
        ('V', 'Volunteer'),
        ('F', 'Faculty')
    )

    email                   = models.EmailField(verbose_name = "email address", max_length = 255, unique = True,)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    desig                   = models.CharField(max_length = 1, choices = DESIG, default = 'V')
    auth                    = models.BooleanField(default = False)  # For authentication by admin
    # active                  = models.BooleanField(default = True)   # Will continue or on pause  (WILL PUT IT IN VOLUN TABLE)
    # confirm = models.BooleanField(default = False) #For email confirmation

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    #Don't use methods name same as attributes name

    # @property
    # def is_admin(self):
    #     return self.is_admin

    # @property
    # def is_staff(self):
    #     return self.is_staff

    # @property
    # def is_active(self):
    #     return self.is_active

    # @property
    # def is_superuser(self):
    #     return self.is_superuser



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Generate a Token everytime a new User registers."""
    if created:
        Token.objects.create(user=instance)
