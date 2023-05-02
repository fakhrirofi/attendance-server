from django.urls import path
from . import views, API

urlpatterns = [
    path('', views.index, name='index'),
    path('form/<event_name>', views.registration, name='registration'),
    path('registered/<enc>', views.registered, name='registered'),
    path('api/<api_type>', API.api_handler, name='api')
]
