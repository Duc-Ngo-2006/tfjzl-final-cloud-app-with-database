from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

# View danh sách khóa học
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        return Course.objects.all()

# View chi tiết khóa học
class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'

# Hàm xử lý khi học viên nộp bài thi (submit)
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    
    # Lấy enrollment của người dùng cho khóa học này
    enrollment = Enrollment.objects.get(user=user, course=course)
    
    # Tạo một Submission mới
    submission = Submission.objects.create(enrollment=enrollment)
    
    # Lấy các đáp án được chọn từ form
    for key, value in request.POST.items():
        if key.startswith('choice_'):
            choice_id = int(value)
            choice = Choice.objects.get(id=choice_id)
            submission.choices.add(choice)
            
    submission.save()
    
    # Chuyển hướng đến trang hiển thị kết quả bài thi
    return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

# Hàm hiển thị kết quả bài thi (show_exam_result)
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    selected_choices = submission.choices.all()
    selected_ids = [choice.id for choice in selected_choices]
    
    total_score = 0
    max_score = 0
    
    # Tính điểm bài thi
    for question in course.question_set.all():
        max_score += question.grade
        if question.is_get_score(selected_ids):
            total_score += question.grade
            
    context = {
        'course': course,
        'selected_ids': selected_ids,
        'total_score': total_score,
        'max_score': max_score,
        'submission': submission
    }
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
