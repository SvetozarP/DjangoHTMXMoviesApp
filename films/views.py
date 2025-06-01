from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, RedirectView
from django.contrib.auth import get_user_model, logout

from films.forms import RegisterForm

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect("index")

def check_username(request):
    username = request.POST.get('username')
    if request.htmx:
        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse('<div style="color: red" id="username-error">This username is already exists.</div>')

        else:
            return HttpResponse('<div style="color: green" id="username-error">This username is available.</div')
    else:
        return redirect("login")