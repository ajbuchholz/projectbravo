from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout
from apps.accounts.forms import *
from django.http import HttpResponseRedirect
from django_htmx.http import HttpResponseClientRedirect
from django.urls import reverse
from core.mixins import AccessModelMixin, HTMXRequiredMixin, PermissionsRequiredMixin
from django.core.mail import send_mail
from django.conf import settings

class LoginView(View):
    def dispatch(self, request):
        if request.user.is_authenticated:
            super().dispatch(request)
            messages.add_message(request, messages.WARNING, "You are already logged in!")
            return HttpResponseRedirect("/")
        return super().dispatch(request)


    def get(self, request):
        form = LoginForm()
        return render(request=request, template_name="accounts/login.html", context={"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.login(request):
            return HttpResponseRedirect(reverse("dashboard"))
        return render(request=request, template_name="accounts/login.html", context={"form": form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        else:
            messages.add_message(request, messages.WARNING, "Can't log out because already logged out!")
        return HttpResponseRedirect(reverse("accounts:login"))


class RegisterView(View):
    def dispatch(self, request):
        if request.user.is_authenticated:
            super().dispatch(request)
            messages.add_message(request, messages.WARNING, "You cannot register an account while being logged in!")
            return HttpResponseRedirect("/")
        return super().dispatch(request)

    def get(self, request):
        form = RegisterForm()
        return render(request=request, template_name="accounts/register.html", context={"form": form})

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            account = form.instance
            verification_link = f"127.0.0.1:8000/accounts/verify/{account.verification_token}"
            subject = "Account Verification"
            message = f"Please click the following link to verify your account: {verification_link}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = form.cleaned_data['email']
            send_mail(subject, message, from_email, [to_email])

            messages.add_message(request, messages.SUCCESS, "An email with a verification link has been sent to your email address.")
            return HttpResponseRedirect(reverse("accounts:login"))
        return render(request=request, template_name="accounts/register.html", context={"form": form})


class VerifyView(View):
    def get(self, request, token):
        try:
            account = Account.objects.get(verification_token=token)
            if not account.is_verified:
                account.is_verified = True
                account.save()
                messages.add_message(request, messages.SUCCESS, "Your account has been verified. You can now log in.")
        except:
            messages.add_message(request, messages.ERROR, "Invalid verification token.")
        return HttpResponseRedirect(reverse("home"))
    
class ListView(PermissionsRequiredMixin, View):
    superuser = True

    def get(self, request):
        accounts = Account.objects.all()
        return render(request=request, template_name="accounts/list.html", context={"accounts": accounts})


class SettingView(PermissionsRequiredMixin, AccessModelMixin, View):
    superuser = True
    personal = True
    model = Account

    def get(self, request):
        form = SettingsForm(instance=self.account)
        return render(request, "accounts/settings.html", {"form": form, "account": self.account,})
    
    def post(self, request):
        form = SettingsForm(request.POST, instance=self.account)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "The account has been successfully edited.")
            return HttpResponseRedirect(reverse("home"))
        return render(request=request, template_name="accounts/settings.html", context={"form": form, "account": self.account})
        

class DeleteView(HTMXRequiredMixin, PermissionsRequiredMixin, AccessModelMixin, View):
    personal = True
    superuser = True
    model = Account

    def get(self, request):
        return render(request=request, template_name="accounts/delete.html", context={"account": self.account})

    def post(self, request):
        self.account.delete()
        messages.add_message(request, messages.SUCCESS, "The account has been deleted.")
        return HttpResponseClientRedirect(reverse("home"))


class PasswordChangeView(HTMXRequiredMixin, PermissionsRequiredMixin, AccessModelMixin, View):
    personal = True
    superuser = True
    model = Account

    def get(self, request):
        form = PasswordChangeForm()
        return render(request=request, template_name="accounts/change_password.html", context={"form": form, "account": self.account})

    def post(self, request):
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            form.save(self.account)
            messages.add_message(request, messages.SUCCESS, "You have successfully changed your password.")
            return HttpResponseClientRedirect(reverse("accounts:login"))
        return render(request=request, template_name="accounts/change_password.html", context={"form": form, "account": self.account})
    
class TypeView(PermissionsRequiredMixin, AccessModelMixin, View):
    superuser = True
    model = Account

    def get(self, request):
        self.account.is_superuser = not self.account.is_superuser
        self.account.save()
        if self.account.is_superuser:
            messages.add_message(
                request, messages.SUCCESS, "The account type has been successfully changed to manager."
            )
        else:
            messages.add_message(
                request, messages.SUCCESS, "The account type has been successfully changed to developer."
            )
        return HttpResponseRedirect(self.next)


class TokenView(PermissionsRequiredMixin, AccessModelMixin, View):
    personal = True
    superuser = True
    model = Account

    def get(self, request):
        return render(request=request, template_name="accounts/access.html", context={"account": self.account})