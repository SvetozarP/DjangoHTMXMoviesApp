from django.db.models import Max
from films.models import UserFilms
from django.db.models import F


def get_max_order(user) -> int:
    existing_films = UserFilms.objects.filter(user=user)
    if not existing_films:
        return 1
    else:
        current_max = existing_films.aggregate(max_order=Max('order'))['max_order']
        return current_max + 1


def reorder(user):
    existing_films = UserFilms.objects.filter(user=user).order_by('order', 'id')  # ensure stable order
    if not existing_films.exists():
        return

    for idx, user_film in enumerate(existing_films, start=1):
        user_film.order = idx

    UserFilms.objects.bulk_update(existing_films, ['order'])