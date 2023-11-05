from django.urls import path
from . import viewss
from .viewss import CourseListView

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('mine/', viewss.ManageCourseListView.as_view(), name='manage_course_list'),
    path('new-grade/<pk>/', viewss.course_new_grade, name='course_new_grade'),
    path('new-grade/<pk>/assos/add', viewss.course_new_grade_assos, name='course_new_grade_assos'),
    path('create/', viewss.CourseCreateView.as_view(), name='course_create'),
    path('<pk>/edit/', viewss.CourseUpdateView.as_view(), name='course_edit'),
    path('<pk>/delete/', viewss.CourseDeleteView.as_view(), name='course_delete'),
    path('<pk>/module/', viewss.CourseModuleUpdateView.as_view(), name='course_module_update'),
    path('module/<int:module_id>/content/<model_name>/create/',	viewss.ContentCreateUpdateView.as_view(), name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/', viewss.ContentCreateUpdateView.as_view(), name='module_content_update'),
    path('content/<int:id>/delete/', viewss.ContentDeleteView.as_view(), name='module_content_delete'),
    path('module/<int:module_id>/', viewss.ModuleContentListView.as_view(), name='module_content_list'),
    path('grade/<int:grade_id>/', viewss.CourseListView.as_view(), name='course_list_grade'),
    path('grade/<int:grade_id>/subject/<slug:subject>/', viewss.CourseListView.as_view(), name='course_list_subject_grade'),
    path('<slug:slug>/', viewss.CourseDetailView.as_view(), name='course_detail'),
    path('see/<pk>/', viewss.StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('see/<pk>/<module_id>/', viewss.StudentCourseDetailView.as_view(), name='student_course_detail_module'),
    path('see/<pk>/<module_id>/question/add/', viewss.student_module_question, name='student_module_question'),
    path('see/<pk>/question/add/', viewss.student_module_question, name='student_question'),
    path('see/<pk>/<module_id>/reply/add/', viewss.student_module_reply, name='student_module_reply'),
    path('see/<pk>/reply/add/', viewss.student_module_reply, name='student_module_reply'),
]