from django.urls import path, re_path,include
from .views import *


urlpatterns = [
    path('aa', aa),
    path("main_inflow",main_inflow),
    path("share_inflow",share_inflow),
    path("order",order)
]