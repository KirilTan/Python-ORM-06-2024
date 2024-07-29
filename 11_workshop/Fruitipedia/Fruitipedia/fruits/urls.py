from django.urls import path, include
from Fruitipedia.fruits import views


urlpatterns = (
    path('', views.index, name="index"),
)
