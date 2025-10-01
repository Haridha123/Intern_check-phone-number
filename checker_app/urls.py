from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/check-single', views.check_single, name='check_single'),
    path('api/session-status', views.session_status, name='session_status'),
]
