from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.apps import apps
from django.forms.models import modelform_factory
from django.views.generic.list import ListView
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course, Module, Content
from .forms import CourseForm, ModuleFormSet, QuestionFormSet
from django import forms
from students.forms import CourseEnrollForm
# Create your views here.


def home(request):
    return render(request, 'formation/home.html')


class CourseListView(ListView):
    model = Course
    template_name = 'formation/courses/list.html'


def login_page(request):
    return render(request, 'formation/registration/login.html')


class CourseDetailView(DetailView):
    model = Course
    template_name = 'formation/courses/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enroll_form"] = CourseEnrollForm(
            initial={'course': self.object})
        return context


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'formation/manage/course/form.html'


class ManageCourseView(OwnerCourseMixin, ListView):
    template_name = 'formation/manage/list.html'
    permission_required = 'formation.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'formation.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'formation.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'formation/manage/course/delete.html'
    permission_required = 'formation.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'formation/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})


class ContentCourseUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'formation/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='formation', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model,
                                 widgets={
                                     'title': forms.TextInput(attrs={'class': 'form-control'}),
                                     'content': forms.Textarea(attrs={'class': 'form-control'}),
                                     'image': forms.FileInput(attrs={'class': 'form-control'}),
                                     'file': forms.FileInput(attrs={'class': 'form-control'}),
                                     'url': forms.URLInput(attrs={'class': 'form-control'}),
                                 },
                                 exclude=[
                                     'owner', 'order', 'created', 'updated'
                                 ]
                                 )
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj,
                             data=request.POST,
                             files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, pk):
        content = get_object_or_404(
            Content, id=pk, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'formation/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(
            Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})


class CourseExamenUpdateView(TemplateResponseMixin, View):
    template_name = 'formation/manage/examens/form.html'
    course = None

    def get_formset(self, data=None):
        return QuestionFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset})
