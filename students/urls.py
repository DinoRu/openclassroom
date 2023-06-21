from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(),
         name='student_registration'),
    path('enroll-course/', views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
    path('courses/', views.StudentCourseListView.as_view(),
         name='student_course_list'),
    path('course/<pk>/', views.StudentCourseDetailView.as_view(),
         name='student_course_detail'),
    path('course/<pk>/<module_id>/', views.StudentCourseDetailView.as_view(),
         name='student_course_detail_module'),
    path('start_examen/<pk>/', views.StudentExaminationView.as_view(),
         name='student_examen_start'),
    path('view_result/<pk>/', views.CalculateMarksView.as_view(),
         name='student_calculate_marks'),
    path('result/', views.ResultView.as_view(),
         name='student_view_exam_result'),
    path('check_marks/<pk>/', views.StudentCheckMarkView.as_view(), name='check_marks'),
    path('student/profile-create/',
         views.StudentProfileCreateView.as_view(), name='profile_create'),
    path('student/profile/', views.StudentProfileView.as_view(), name='profile'),
    path('student/profile/update',
         views.StudentProfileUpdateView.as_view(), name='profile_update'),
]
