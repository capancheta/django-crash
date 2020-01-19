from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.shortcuts import redirect
from accounts.forms import UpdateForm
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist


class UserUpdateView(UpdateView):
    model = User
    form_class = UpdateForm
    context_object_name = 'user'
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, f):
        u = f.save(commit=False)
        p = u.profile
        p.avatar = f.cleaned_data.get('avatar')
        p.save()
        return redirect('profile')

    def get_context_data(self, **kwargs):
        try:
            p = Profile.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            p = Profile.objects.create(
                user=self.request.user
            )
        self.kwargs['profile'] = p  # bind data
        self.initial['avatar'] = p.avatar  # flood extra fields
        return super().get_context_data(**kwargs)

