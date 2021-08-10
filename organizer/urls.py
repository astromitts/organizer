from django.urls import path
from django.views.generic import TemplateView
from organizer import views


urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
]
