from django.contrib import admin
from django.urls import path

from home.views import (
    home_screen_view,
)

from account.views import(
    authenticate_view,
    login_view,
    register_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name="home"),

    # authenticate
    path('authenticate/', authenticate_view, name="authenticate"),
    # login
    path('authenticate/login/<int:account_id>/', login_view, name="login"),
    # register
    path('authenticate/register/<str:phone_number>/', register_view, name="register"),
]
