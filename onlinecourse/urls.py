from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Route danh sách & chi tiết khóa học
    path('', views.CourseListView.as_view(), name='index'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),
    
    # Route nộp bài thi (submit)
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Route hiển thị kết quả bài thi (show_exam_result)
    path('course/<int:course_id>/submission/<int:submission_id>/result/', 
         views.show_exam_result, name='show_exam_result'),
]
