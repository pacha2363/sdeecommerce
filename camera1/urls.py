from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.camera_page, name="camera"),
    #path('register/', views.register_page, name="register"),

]