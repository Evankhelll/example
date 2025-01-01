# publik/urls.py

from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # other paths for your app
    path('', views.fe_index, name='fe_index'),
    path('upload/', views.fe_upload, name='fe_upload'),
    path('review/', views.fe_review, name='fe_review'),
]