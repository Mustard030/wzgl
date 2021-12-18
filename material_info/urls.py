from django.urls import path
from . import views

urlpatterns = [
       path('mater_mg/', views.dispatcher),
]