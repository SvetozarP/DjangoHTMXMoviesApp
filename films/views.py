from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, RedirectView
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods

from films.forms import RegisterForm
from films.models import Film
from django.views.generic.list import ListView

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
            return HttpResponse('<div class="error" id="username-error">This username is already exists.</div>')

        else:
            return HttpResponse('<div class="success" id="username-error">This username is available.</div')
    else:
        return redirect("login")

class FilmList(ListView, LoginRequiredMixin):
    template_name = 'films.html'
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        user = self.request.user
        return user.films.all()


@login_required
def add_film(request):
    name = request.POST.get('filmname')
    film = Film.objects.get_or_create(name=name)[0]

    #add film to users list
    request.user.films.add(film)

    #return template with user's films
    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})

@login_required
@require_http_methods(['DELETE'])
def delete_film(request, pk):
    # remove the film from the list
    request.user.films.remove(pk)
    # return the list after deletion
    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})

@login_required
@require_http_methods(['POST'])
def search_film(request):
    search_text = request.POST.get('search')

    results = Film.objects.filter(name__icontains=search_text)
    context = {'results': results}

    return render(request, 'partials/search-results.html', context)