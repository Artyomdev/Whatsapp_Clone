
from unicodedata import name
from django.contrib import admin
from django.urls import path
from .views import *
app_name="asd"

urlpatterns = [
    path('login/' , loginview),
    path('<str:room_name>/', roomview, name='room'),
    path('api' , imgpost),
    path('', index , name="chat"),
    path('get_room/<int:id>' ,get_room ),
]
