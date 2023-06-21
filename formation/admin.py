from django.contrib import admin
from .models import Subject, Course, Module, Question, Result

# Register your models here.


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title', )}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'created']
    list_filter = ['level', 'created', 'updated']
    prepopulated_fields = {'slug': ('title', )}
    inlines = [ModuleInline]


admin.site.register(Question)
admin.site.register(Result)
