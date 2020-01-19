from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from .forms import SignUpForm, UpdateForm
from django.views.generic import CreateView
from django.contrib.auth.models import User


def index(r):
    if r.method == 'POST':
        f = SignUpForm(r.POST)
        if f.is_valid():
            u = f.save()
            login(r, u)
            return HttpResponseRedirect(reverse('main_board'))
    else:
        f = SignUpForm()
    return render(r, 'signup.html', {'form': f})


class UserCreateView(CreateView):
    model = User
    form_class = SignUpForm
    context_object_name = 'user'
    template_name = 'signup.html'

    def form_valid(self, f):
        u = f.save()
        login(self.request, u)
        return HttpResponseRedirect(reverse('main_board'))

    # def get_context_data(self, **kwargs):
        # modify if you want to change the {% form %} context tags in the html
        # if 'form' not in kwargs:
        #    kwargs['form'] = self.get_form()
        # return super().get_context_data(**kwargs)




