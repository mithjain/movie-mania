from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from movie_mania.utils import get_clean_url

app_name = 'movie_mania'

urlpatterns = [

    path('movies/', include('movies.urls', namespace='movies')),
]

urlpatterns += static(get_clean_url(settings.BASE_URL) + settings.STATIC_URL, document_root=settings.STATIC_ROOT)
