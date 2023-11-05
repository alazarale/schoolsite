from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news, name='news_list'),
    path('news/<pk>/', views.news_detail, name='news_detail'),
]
