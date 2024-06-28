from django.urls import path
from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("", views.ListView.as_view(), name="list"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("<int:uid>/type/", views.TypeView.as_view(), name="type"),
    path("settings/<int:uid>/", views.SettingView.as_view(), name="settings"),
    path("delete/<int:uid>/", views.DeleteView.as_view(), name="delete"),
    path("<int:uid>/change", views.PasswordChangeView.as_view(), name="password_change"),
    path("verify/<str:token>/", views.VerifyView.as_view(), name="verify"),
    path("tokens/<int:uid>/", views.TokenView.as_view(), name="tokens"),
]