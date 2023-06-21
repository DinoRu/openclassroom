from django.urls import path
from . import views

urlpatterns = [
    path('mine/', views.ManageCourseView.as_view(), name='manage_course_list'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<pk>/edit', views.CourseUpdateView.as_view(), name='course_update'),
    path('delete/<pk>/', views.CourseDeleteView.as_view(), name='course_delete'),
    path('', views.home, name='home'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='detail'),
    path('<pk>/module/', views.CourseModuleUpdateView.as_view(),
         name='course_module_update'),
    path('module/<int:module_id>/content/<model_name>/create/',
         views.ContentCourseUpdateView.as_view(), name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',
         views.ContentCourseUpdateView.as_view(), name='module_content_update'),
    path('content/<pk>/delete/', views.ContentDeleteView.as_view(),
         name='module_content_delete'),
    path('module/<int:module_id>/', views.ModuleContentListView.as_view(),
         name='module_content_list'),
    path('<pk>/examen/', views.CourseExamenUpdateView.as_view(),
         name='course_examen_update'),
]
