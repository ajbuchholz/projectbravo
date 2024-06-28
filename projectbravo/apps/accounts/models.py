from pydoc import importfile
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from apps.accounts.managers import AccountManager
from django.conf import settings
import secrets


class Account(AbstractBaseUser):
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, error_messages={"unique": "This email is already in use."})
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = models.CharField(max_length=16, blank=True, help_text="Must not have any spaces, parentheses, or dashes")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Must be formatted as YYYY-MM-DD")
    company = models.CharField(max_length=64, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, blank=True)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    
    # admin and important account info
    is_superuser = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["first_name"]

    @property
    def avatar_url(self):
        if self.avatar:
            return settings.STATIC_URL + self.avatar.url
        return settings.STATIC_URL + "avatars/profile.png"

    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
    def save(self, *args, **kwargs):
        if not self.verification_token:
            self.verification_token = secrets.token_hex(32)
        super().save(*args, **kwargs)

