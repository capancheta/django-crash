from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('', views.index, name='new_user')
    path('', views.UserCreateView.as_view(), name='new_user'),
]