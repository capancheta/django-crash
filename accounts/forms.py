from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'Please enter a valid email address.'}),
        max_length=254,
        required=True
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UpdateForm(UserChangeForm):
    password = None
    avatar = forms.CharField(max_length=2083, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'avatar')
