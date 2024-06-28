import re
from apps.accounts.models import Account
from django import forms
from django.contrib.auth import authenticate, login
from django.conf import settings
from datetime import datetime

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False))

    def clean(self):
        if self._errors:
            return
        self.account = authenticate(email=self.cleaned_data["email"], password=self.cleaned_data["password"])
        if self.account is None:
            raise forms.ValidationError("The email and/or password you entered are incorrect.")
        return self.cleaned_data

    def login(self, request):
        if self.is_valid():
            login(request, self.account)
            return True
        return False

class RegisterForm(forms.ModelForm):
    verify_email = forms.EmailField(label="Verify Email")
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        help_text="Must have at least 8 characters, a letter, and a number",
    )
    verify_password = forms.CharField(label="Verify Password", widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = Account
        fields = (
            "email",
            "verify_email",
            "password",
            "verify_password",
        )

    def clean_password(self):
        if not re.match(settings.PASSWORD_REGEX, self.cleaned_data["password"]):
            raise forms.ValidationError("The password needs to have at least 8 characters, a letter, and a number.")
        return self.cleaned_data["password"]

    def clean(self):
        self.cleaned_data = super().clean()
        if self.cleaned_data.get("password") and self.cleaned_data.get("verify_password"):
            if self.cleaned_data["password"] != self.cleaned_data["verify_password"]:
                raise forms.ValidationError(_("The passwords do not match."))
        if self.cleaned_data.get("email") and self.cleaned_data.get("verify_email"):
            if self.cleaned_data["email"] != self.cleaned_data["verify_email"]:
                raise forms.ValidationError(_("The emails do not match."))
        return self.cleaned_data

    def save(self):
        account = super().save(commit=False)
        account.is_superuser = False
        account.set_password(self.cleaned_data["password"])
        account.save()
        return account


class SettingsForm(forms.ModelForm):
    verify_email = forms.EmailField(label="Verify Email")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)

    class Meta:
        model = Account
        fields = (
            "avatar",
            "email",
            "verify_email",
            "first_name",
            "last_name",
            "date_of_birth",
            "company",
            "phone",
        )
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "date_of_birth": "Date of Birth",
            "company": "Company",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["verify_email"].initial = self.instance.email


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput(render_value=False))
    verify_new_password = forms.CharField(label="Verify New Password", widget=forms.PasswordInput(render_value=False))

    def clean_new_password(self):
        if not re.match(settings.PASSWORD_REGEX, self.cleaned_data["new_password"]):
            raise forms.ValidationError("The password needs to have at least 8 characters, a letter, and a number.")
        return self.cleaned_data["new_password"]

    def clean(self):
        if self._errors:
            return
        if self.cleaned_data["new_password"] != self.cleaned_data["verify_new_password"]:
            raise forms.ValidationError("The passwords do not match.")
        return self.cleaned_data

    def save(self, account):
        account.set_password(self.cleaned_data["new_password"])
        account.save()
        return account

