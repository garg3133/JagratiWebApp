from django.db import models
from django.contrib.auth.models import(
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active = True, is_staff = False, is_admin = False):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using = self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password = password,
            is_active = True,
            is_staff = True,
        )
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password = password,
            is_active = True,
            is_staff = True,
            is_admin = True,
        )
        return user


class User(AbstractBaseUser):
    DESIG = (
        ('V', 'Volunteer'),
        ('F', 'Faculty')
    )
    email = models.EmailField(
        verbose_name = "email address",
        max_length = 255,
        unique = True,
    )
    desig = models.CharField(max_length = 1, choices = DESIG, default = 'V')
    auth = models.BooleanField(default = False)
    active = models.BooleanField(default = True) 
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False) 
    confirm = models.BooleanField(default = False) #For email confirmation

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_confirm(self):
        return self.confirm