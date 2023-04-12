from django.contrib import admin
from django.urls import path

from home.views import home_screen_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name="home"),
]
