from django.urls import re_path, path
from . import views

app_name = 'mainapp'
urlpatterns = [
    re_path(r'^home/$', views.home, name='home'),
    #path('about-us/', views.about_us, name='about_us'),
    #path('facilities/', views.facilities, name='facilities'),
    #path('facilities/other/', views.under_const, name='under_const'),
]
