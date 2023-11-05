from django.urls import path
from . import views

app_name = 'exam_url'
urlpatterns = [
    path('adminpanel/exams/', views.exams, name='exams'),
    path('adminpanel/exams/<pk>/questions/', views.exam_questions, name='exam_questions'),
    path('adminpanel/exams/<pk>/questions/add/', views.exam_questions_add, name='exam_questions_add'),
    path('adminpanel/exams/<pk>/questions/add-modules/', views.exam_questions_add_modules, name='exam_questions_add_modules'),
    path('adminpanel/exams/<pk>/questions/add-modules/add/', views.exam_questions_add_modules_add, name='exam_questions_add_modules_add'),
    # path('rounds/', views.round_select, name='round_list'),
    # path('rounds-result/', views.res_rounds, name='res_round'),
    # path('rounds-result/<pk>/', views.res_rounds_exam, name='res_round_exam'),
    # path('rounds-result/det/<exam_pk>/', views.res_rounds_exam_det, name='res_round_exam_det'),
    # path('rounds/<pk>/examlist/', views.exam_list, name='exam_list'),
    # path('rounds/<pk>/examlist/<exam_pk>/', views.exam_list_sp, name='exam_list_sp'),
    # path('rounds/<pk>/examlist/<exam_pk>/results/', views.exam_list_sp_res, name='exam_list_sp_res'),
    # path('examlist/', views.stud_exam_list, name='stud_exam_list'),
    # path('exam/take/exam45345<pk>2453/', views.exam_take_detail, name='exam_take_detail'),
    # path('exam/take/exam/not-fooled/', views.not_fooled, name='not_fooled'),
    # path('exam/take/exam/result3244353<pk>4646456/', views.exam_result, name='exam_result'),
    # path('exam/take/exam45345<pk>2453/exam/submit/', views.exam_submit, name='exam_submit'),
    # path('examlist/<pk>/', views.stud_exam_list_sub, name='stud_exam_list_sub'),
    # path('exam/<pk>/', views.exam_list_sp, name='exam_list_sp'),
    # path('exam/<pk>/statup/', views.exam_statup, name='exam_statup'),
    # path('exam/<pk>/question/add/', views.exam_ques_add, name='exam_ques_add'),
]
