from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, RedirectView
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from films.forms import RegisterForm
from films.models import Film, UserFilms
from films.utils import get_max_order, reorder
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
        return UserFilms.objects.filter(user=self.request.user)


@login_required
def add_film(request):
    name = request.POST.get('filmname')
    film = Film.objects.get_or_create(name=name)[0]

    #add film to users list
    if not UserFilms.objects.filter(film=film, user=request.user).exists():
        UserFilms.objects.create(user=request.user, film=film, order=get_max_order(request.user))

    #return template with user's films
    films = UserFilms.objects.filter(user=request.user)
    messages.success(request, f'Added {name} to list of films')
    context = {
        'films': films,
    }
    return render(request, 'partials/film-list.html', context)


@login_required
@require_http_methods(['DELETE'])
def delete_film(request, pk):
    # remove the film from the list
    UserFilms.objects.get(pk=pk).delete()

    reorder(request.user)

    # return the list after deletion
    films = UserFilms.objects.filter(user=request.user)
    return render(request, 'partials/film-list.html', {'films': films})


@login_required
@require_http_methods(['POST'])
def search_film(request):
    search_text = request.POST.get('search')

    userfilms = UserFilms.objects.filter(user=request.user)
    results = Film.objects.filter(name__icontains=search_text).exclude(
        name__in=userfilms.values_list('film__name', flat=True)
    )
    context = {'results': results}

    return render(request, 'partials/search-results.html', context)


def clear(request):
    return HttpResponse('')


@login_required
def sort(request):
    film_pks_order = request.POST.getlist('film_order')
    films = []
    for idx, film_pk in enumerate(film_pks_order, start=1):
        userfilm = UserFilms.objects.get(pk=film_pk)
        userfilm.order = idx
        userfilm.save()
        films.append(userfilm)

    return render(request, 'partials/film-list.html', {'films': films})