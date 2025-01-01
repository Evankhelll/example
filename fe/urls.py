# publik/urls.py

from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # other paths for your app
    path('', views.publik_index_view, name='publik_index'),
    path('runcommand/', views.RunCommandView.as_view(), name='run-command'),
    path('artist/<int:artist>/', views.publik_artist_view, name='artist_index'),
    path('hash', views.hash_password, name='hash'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('sitemap.xml', TemplateView.as_view(template_name='publik/sitemap.xml', content_type='application/xml')),
    path('robot.txt', TemplateView.as_view(template_name='publik/robot.txt', content_type='text/plain')),
]