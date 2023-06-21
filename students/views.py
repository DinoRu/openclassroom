from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserCreateForm, CourseEnrollForm, MarqueCompleteForm, StudentProfileForm
from formation.models import Course, Question, Result
from students.models import Student

# Create your views here.


class StudentRegistrationView(CreateView):
    form_class = UserCreateForm
    template_name = 'students/registration/registration.html'
    success_url = reverse_lazy('student_dashboard')

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/formations/dashboard.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/formations/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            context["module"] = course.modules.all()[0]

        module = context["module"]
        # Tri des modules du cours
        sorted_modules = list(course.modules.order_by('id'))

        # Recherche de l'index du module actuel
        current_module_index = sorted_modules.index(module)

        # Récupération des modules précédents et suivants
        previous_module = sorted_modules[current_module_index -
                                         1] if current_module_index > 0 else None
        next_module = sorted_modules[current_module_index +
                                     1] if current_module_index < len(sorted_modules) - 1 else None

        context['previous_module'] = previous_module
        context['next_module'] = next_module
        context['completion_form'] = MarqueCompleteForm(
            initial={'complet': module.complet})
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        module = self.get_context_data()['module']
        complet = form.cleaned_data['complet']

        if complet:
            next_module = self.get_context_data()['next_module']
            if next_module:
                return redirect('student_course_detail_module', args=[self.get_object().id, next_module.id])
        return response


class StudentExaminationView(TemplateResponseMixin, View):
    template_name = 'students/examens/examination.html'
    course = None

    def get(self, request, pk):
        self.course = get_object_or_404(Course, id=pk)
        questions = Question.objects.filter(course=self.course)
        return self.render_to_response({'course': self.course, 'questions': questions})

    def post(self, request, pk):
        self.course = get_object_or_404(Course, id=pk)
        questions = Question.objects.filter(course=self.course)

        total_marks = 0
        obtained_marks = 0
        for i in range(len(questions)):
            selected_ans = request.POST.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                obtained_marks += questions[i].mark
            total_marks += questions[i].mark
        percentage = (obtained_marks / total_marks) * 100
        result = Result()
        result.marks = percentage
        result.exam = self.course
        result.student = request.user
        result.save()
        return redirect('student_course_list')


class CalculateMarksView(TemplateResponseMixin, View):
    course = None

    def post(self, request, pk):
        self.course = get_object_or_404(Course, id=pk)
        questions = Question.objects.all().filter(course=self.course)

        total_marks = 0
        for i in range(len(questions)):
            selected_ans = request.POST.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks += questions[i].mark
        result = Result()
        result.marks = total_marks
        result.exam = self.course
        result.student = request.user
        result.save()
        return redirect('check_marks', self.course.id)


class ResultView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        return render(request, 'students/examens/view_result.html', {'courses': courses})


class StudentCheckMarkView(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        student = request.user
        results = Result.objects.filter(exam=course).filter(student=student)
        return render(request, 'students/examens/check_marks.html', {'results': results})


class StudentProfileCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = StudentProfileForm()
        return render(request, 'students/profile/profile_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            student = form.save(commit=False)
            student.user = user
            student.save()
            return redirect('student_course_list')
        return render(request, 'students/profile/profile_form.html', {'form': form})


class StudentProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        return render(request, 'students/profile/profile.html', {'student': student})


class StudentProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = StudentProfileForm(instance=request.user.student)
        return render(request, 'students/profile/profile_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StudentProfileForm(
            request.POST, request.FILES, instance=request.user.student)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'students/profile/profile_form.html', {'form': form})
