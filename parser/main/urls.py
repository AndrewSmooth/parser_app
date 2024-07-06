from django.contrib import admin
from django.urls import include, path

from .views import index, parsing

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('parsing/', parsing, name='parsing'),
]