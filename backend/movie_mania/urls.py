from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView


app_name = 'movie_mania'

urlpatterns = [
    path(
        settings.BASE_URL,
        include([

        ]))
]

