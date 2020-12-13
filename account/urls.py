from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_page, name="dashboard"),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('myprofile/', views.myprofile_page, name="myprofile"),
    path('createaccount/', views.createaccount_page, name="createaccount"),
    #path('downloadQRCode/<hereur_id>', downloadQRCode, name='downloadQRCode'),
]