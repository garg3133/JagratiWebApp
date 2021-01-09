from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):  # Add all required fields
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    DESIG = (
        ('v', 'Volunteer'),
        ('f', 'Faculty')
    )

    email = models.EmailField(verbose_name="Email Address", max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    auth = models.BooleanField(default=False)
    desig = models.CharField(max_length=1, choices=DESIG, default='v')
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []   # Required for 'createsuperuser'

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """For cpanel."""
        self.is_active = (self.is_active is True)
        self.is_staff = (self.is_staff is True)
        self.is_superuser = (self.is_superuser is True)
        self.auth = (self.auth is True)

        super(User, self).save(*args, **kwargs)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Generate a Token everytime a new User registers."""
    if created:
        Token.objects.create(user=instance)


class Profile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name="First Name",max_length=50)
    last_name = models.CharField(verbose_name="Last name",max_length=50)
    profile_image = ProcessedImageField(
        upload_to='profile_pics', processors=[ResizeToFill(300,300)],
        format='JPEG', options={'quality': 60}, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    alt_email = models.EmailField(verbose_name="Alternate Email", max_length=255, blank=True)
    contact_no = models.CharField(verbose_name="Contact Number", max_length=13)
    street_address1 = models.CharField(verbose_name="Address Line 1", max_length=255)
    street_address2 = models.CharField(verbose_name="Address Line 2", max_length=255, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.get_full_name} - {self.user.email}'

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def get_complete_address(self):
        if self.street_address2:
            return f'{self.street_address1}, {self.street_address2}, {self.city} - {self.pincode}, {self.state}'
        return f'{self.street_address1}, {self.city} - {self.pincode}, {self.state}'

    @property
    def get_profile_image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        elif self.gender == 'F':
            return "/static/home/images/woman.png"
        else:
            return "/static/home/images/man.png"

class AuthorisedDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('user', 'device_id'),)

    def __str__(self):
        return f'{self.user.email} - {self.device_id}'
