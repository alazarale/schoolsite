from django.urls import re_path, path
from . import views

app_name = 'mainapp'
urlpatterns = [
    re_path(r'^adminpanel/$', views.adminpanel, name='admin_main'),
    re_path(r'^adminpanel/grades/$', views.admingrade, name='admin_grades'),
    re_path(r'^adminpanel/students/$', views.adminstudent, name='admin_students'),
    path('adminpanel/grades/<pk>/edit/', views.admingrade_edit, name='admin_grades_edit'),
    path('adminpanel/grades/<pk>/edit/update/', views.admingrade_edit_ajax, name='admin_grades_edit_ajax'),
    
    path('adminpanel/students/3246<pk>353/profile/', views.adminstudent_profile, name='admin_student_profile'),
    path('adminpanel/students/3246<pk>353/profile/att/', views.adminstudent_profile_att, name='admin_student_profile_att'),
    
    path('adminpanel/teachers/', views.adminteacher, name='admin_teacher'),
    path('adminpanel/teachers/add/', views.adminteacher_add, name='admin_teacher_add'),
    path('adminpanel/teachers/add/add/', views.adminteacher_add_json, name='admin_teacher_add_json'),
    path('adminpanel/teachers/434<pk>4232/profile/', views.adminteacher_profile, name='admin_teacher_profile'),
    path('adminpanel/teachers/434<pk>4232/profile/add-grade/', views.adminteacher_profile_home, name='admin_teacher_profile_home'),
    path('adminpanel/teachers/434<pk>4232/profile/get/', views.adminteacher_get, name='admin_teacher_get'),
    path('adminpanel/teachers/434<pk>4232/profile/add-sub/', views.adminteacher_subadd, name='admin_teacher_subadd'),
    
    path('adminpanel/parents/', views.adminparent, name='admin_parent'),
    path('adminpanel/parents/new/', views.adminparent_add, name='admin_parent_add'),
    path('adminpanel/parents/new/<pk>/link/', views.adminparent_add_link, name='admin_parent_add_link'),
    path('adminpanel/parents/new/<pk>/link/get/', views.adminparent_add_link_get, name='admin_parent_add_link_get'),
    path('adminpanel/parents/new/<pk>/link/add/', views.adminparent_add_link_add, name='admin_parent_add_link_add'),
    
    path('adminpanel/subjects/', views.adminsubjects, name='admin_subjects'),
    path('adminpanel/subjects/add/', views.adminsubjects_add, name='admin_subject_add'),
    
    path('teacher-acc/teaching-list/', views.teaching_list, name='teaching_list'),
    path('teacher-acc/<sub>/4353<pk>856/', views.teaching_sub_see_all, name='teaching_sub_see'),
    path('teacher-acc/<sub>/4353<pk>856/submitted/', views.submitted_grades_self, name='submitted_grades_self'),
    path('teacher-acc/<sub>/4353<pk>856/submitted/<numb>/add/', views.submitted_grades_self_add, name='submitted_grades_self_add'),
    path('teacher-acc/<sub>/4353<pk>856/submitted/<numb>/add/add/', views.submitted_grades_self_json, name='submitted_grades_self_json'),
    path('teacher-acc/<sub>/4353<pk>856/add-result/', views.teaching_sub_add, name='teaching_sub_add'),
    path('teacher-acc/<sub>/4353<pk>856/784<pk2>65/', views.teaching_sub_res_fill, name='teaching_sub_res_fill'),
    path('teacher-acc/<sub>/4353<pk>856/784<pk2>65/add/', views.teaching_sub_res_fill_json, name='teaching_sub_res_fill_json'),
    
    path('teacher-acc/homeclass/attendance/', views.homeclass_attendance, name='homeclass_attendance'),
    path('teacher-acc/homeclass/<pk>/attendance/take/', views.attendance_take, name='attendance_take'),
    path('teacher-acc/homeclass/<pk>/attendance/take/add/', views.attendance_take_add, name='attendance_take_add'),
    
    path('student-acc/all-results/', views.results_all, name='results_all'),
    path('student-acc/submitted-results/', views.results_submitted, name='results_submitted'),


]
