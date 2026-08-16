from django.contrib import admin

# 1. Import đủ 7 classes từ models
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


# 2. Định nghĩa ChoiceInline
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


# 3. Định nghĩa QuestionInline
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2


# 4. Định nghĩa QuestionAdmin với ChoiceInline
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'grade']


# 5. Định nghĩa LessonAdmin với QuestionInline
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'course']
    inlines = [QuestionInline]


# 6. Định nghĩa CourseAdmin với LessonInline
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


# Đăng ký các Model vào Trang Quản trị (Admin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
