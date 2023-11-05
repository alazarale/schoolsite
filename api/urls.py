from django.conf.urls import url
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('stud/', views.StudentAPIView.as_view()),
    path('teacher/', views.TeacherAPIView.as_view()),
    path('teacher/homeroom/<pk>/attendance/', views.TeacherHRAttendaceAPIView.as_view()),
    path('teacher/homeroom/<pk>/', views.TeacherHR.as_view()),
    path('teacher/homeroom/<pk>/attendance/', views.TeacherHRAttendance.as_view()),
    path('teacher/homeroom/<pk>/attendance/istaken/', views.TeacherHRAttTaken.as_view()),
    path('teacher/homeroom/<pk>/attendance/take/', views.TeacherHRAttTake.as_view()),
    path('teacher/homeroom/<pk>/studs/', views.TeacherHRStudsAPIView.as_view()),
    path('teacher/homeroom/<pk>/class_score/', views.TeacherHRClassScoreAPIView.as_view()),

    path('teacher/teaching/<pk>/', views.TeacherTeaching.as_view()),
    path('teacher/teaching/<pk>/studs/', views.TeacherStudsAPIView.as_view()),
    path('teacher/teaching/<pk>/result/', views.ResultAddAPIView.as_view()),
    path('teacher/teaching/<pk>/result/submit/', views.ResultSumitAPIView.as_view()),
    path('teacher/teaching/<pk>/homework/', views.TeacherHomeworkAPIView.as_view()),
    path('teacher/teaching/<pk>/homework/add/', views.TeacherHomeworkAddAPIView.as_view()),

    path('teacher/teaching/<pk>/submitted/', views.TeacherSubmittedAPIView.as_view()),
    path('teacher/teaching/<pk>/submitted/add/', views.TeacherSubmittedAddAPIView.as_view()),

    path('teacher/teaching/<pk>/course/', views.TeacherCourseAPIView.as_view()),
    path('teacher/teaching/<pk>/course/see/', views.TeacherCourseSeeAPIView.as_view()),
    path('teacher/teaching/<pk>/course/<mpk>/modules/', views.TeacherCourseModuleSeeAPIView.as_view()),
    path('teacher/teaching/<pk>/course/<mpk>/modules/add/', views.TeacherCourseModuleAddAPIView.as_view()),

    path('teacher/homeroom/<pk>/attendance/take/', views.TeacherHRAttendaceTakeAPIView.as_view()),

    path('student/subjects/', views.StudentSubjectAPIView.as_view()),
    path('student/homeworks/', views.StudentHomeworkAPIView.as_view()),
    path('student/grade-report/', views.StudentGradeReportAPIView.as_view()),
    path('student/attendances/', views.StudentAttendanceAPIView.as_view()),
    path('student/timetables/', views.StudentTimetableAPIView.as_view()),
    path('student/school-payment/', views.SchoolPaymentAPIView.as_view()),
    path('student/subject/<pk>/homework/', views.StudentSubjectHomeworkAPIView.as_view()),
    path('student/subject/<pk>/all-results/', views.StudentSubjectResultsAPIView.as_view()),
    path('student/subject/<pk>/report/', views.StudentSubjectReportAPIView.as_view()),
    path('student/subject/<pk>/exam/', views.StudentExamAPIView.as_view()),
    path('student/subject/<pk>/exam/<pk2>/take/', views.StudentExamSeeAPIView.as_view()),

    path('parent/', views.ParentAPIView.as_view()),
    path('parent/stud/<pk>/', views.ParentStudAPIView.as_view()),
    path('parent/stud/<pk>/result/', views.ParentStudSubAPIView.as_view()),
    path('parent/stud/<pk>/result/<pk2>/', views.ParentStudSubResultAPIView.as_view()),
    path('parent/stud/<pk>/submitted/<pk2>/', views.ParentSubmittedSubResultAPIView.as_view()),
    path('parent/stud/<pk>/submitted/all/get/', views.ParentGradeReportAPIView.as_view()),
    path('parent/stud/<pk>/attendance/', views.ParentAttendanceAPIView.as_view()),
    path('parent/stud/<pk>/homework/<pk2>/', views.ParentSubjectHomeworkAPIView.as_view()),
    path('parent/stud/<pk>/homework/all/get/', views.ParentHomeworkAPIView.as_view()),
    path('parent/stud/<pk>/timetable/', views.ParentTimetableAPIView.as_view()),
    path('parent/stud/<pk>/payment/', views.ParentPaymentAPIView.as_view()),

    path('student/<pk>/profile/', views.StudentProfileAPIView.as_view()),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
