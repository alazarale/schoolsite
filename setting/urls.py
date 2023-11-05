from django.urls import path
from . import views

urlpatterns = [
    path('setting/add-grades/', views.setting_grade, name='setting_grade'),
    path('setting/add-student/', views.setting_student, name='setting_student'),
    path('setting/add-subject/', views.setting_subject, name='setting_subject'),
    path('setting/subject-list/', views.subject_list, name='subject_list'),
    path('setting/grades-list/', views.grade_list, name='setting_grade_list'),

]