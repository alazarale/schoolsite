from django.urls import re_path, path
from . import views

app_name = 'mainapp'
urlpatterns = [
    re_path(r'^adminpanel/create-year/$', views.acc_yr_setup, name='yr_setup'),
    path('adminpanel/create-grade/768787<pk>43/', views.yr_setup_grades, name='yr_setup_grade'),
    path('adminpanel/create-grade/768787<pk>43/grade/add/', views.add_grades_json, name='add_grade'),
    path('adminpanel/create-subject/2362527<pk>43/', views.yr_setup_subjects, name='yr_setup_subject'),
    path('adminpanel/create-subject/2362527<pk>43/subjects/add/', views.add_subjects_json, name='add_subject'),
    path('adminpanel/create-students/2362527<pk>43/', views.yr_setup_students, name='yr_setup_students'),
    path('adminpanel/create-students/2362527<pk>43/students/add/', views.add_students_json, name='add_students'),
]
