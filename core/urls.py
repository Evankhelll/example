from django.urls import path, include
from . import views
from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register("gambar", api.gambarViewSet)
router.register("komentar", api.komentarViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),  # Must use a list
    # path('dominant-colors/<int:id>/', views.get_colors_as_json, name='dominant_colors'),
    path('dominant-colors2/<int:id>/', views.get_colors_as_json2, name='dominant_colors2'),
]
