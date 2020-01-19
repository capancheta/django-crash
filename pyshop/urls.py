"""pyshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path, reverse_lazy
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('board/', include('board.urls')),
    path('settings/', include('settings.urls')),
    path('signup/', include('accounts.urls')),
    path('logout/', views.LogoutView.as_view(), name='sign_out'),
    re_path(r'[accounts/]*login/', views.LoginView.as_view(template_name='login.html'), name='sign_in'),
    path('reset/', views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='reset_email.html',
            subject_template_name='reset_subject.txt',
            success_url=reverse_lazy('reset_email_sent'),
            ),
        name='reset_send'),
    path('reset/complete/', views.PasswordResetCompleteView.as_view(
            template_name='reset_complete.html'),
        name='reset_complete'),
    path('reset/done/', views.PasswordResetDoneView.as_view(
            template_name='reset_link_sent.html'),
        name='reset_email_sent'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.PasswordResetConfirmView.as_view(
            template_name='reset_confirm.html',
            success_url=reverse_lazy('reset_complete'),
            ),
        name='reset_confirm'),
]
