import jwt

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, username,  mobile, email=None, password=None, gender=None):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')

        if mobile is None:
            raise TypeError('Users must have an mobile.')

        user = self.model(username=username, mobile=mobile, email=self.normalize_email(email))
        user.set_password(password)
        user.gender = gender
        user.save()
        return user

    def create_superuser(self, username, mobile, password=None, email=None, gender=None):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, mobile,  email, password)
        user.is_superuser = True
        user.is_staff = True
        user.gender = gender
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    GENDER = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.BigIntegerField(unique=True, db_index=True)
    gender = models.CharField(choices=GENDER, max_length=50 ,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return '%s - %s' % (self.id, self.name)

    def __str__(self):
        return '%s - %s' % (self.id, self.mobile)

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.username

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=5)

        token = jwt.encode({
            'mobile': self.mobile,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class LoginOtpLog(models.Model):
    mobile = models.BigIntegerField()
    otp = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0}, {1}".format(self.mobile, self.otp)

    def __str__(self):
        return "{0}, {1}".format(self.mobile, self.otp)
