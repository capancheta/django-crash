from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as cbv

urlpatterns = [
    path('password/', cbv.PasswordChangeView.as_view(
        template_name='password_update.html',
        success_url=reverse_lazy('password_updated'),
    ),
         name='password_update'),
    path('password/done/', cbv.PasswordChangeDoneView.as_view(
        template_name='password_update_done.html'),
         name='password_updated'),
    path('profile/', views.UserUpdateView.as_view(), name='profile')
]