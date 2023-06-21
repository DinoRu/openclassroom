from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module, Question


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['subject', 'title', 'slug', 'overview',
                  'description', 'level', 'learn_hours']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'overview': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'learn_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }


ModuleFormSet = inlineformset_factory(Course, Module, fields=['title', 'overview'],
                                      widgets={'title': forms.TextInput(attrs={'class': 'form-control custom-label'}),
                                               'overview': forms.Textarea(attrs={'class': 'form-control'}),
                                               },
                                      extra=2, can_delete=True
                                      )


QuestionFormSet = inlineformset_factory(Course, Question, fields=['question', 'option_1', 'option_2', 'option_3', 'option_4', 'answer', 'mark'],
                                        labels={
                                            'answer': 'Control answer'
},
    widgets={'question': forms.Textarea(attrs={'class': 'form-control custom-label'}),
             'option_1': forms.TextInput(attrs={'class': 'form-control'}),
             'option_2': forms.TextInput(attrs={'class': 'form-control'}),
             'option_3': forms.TextInput(attrs={'class': 'form-control'}),
             'option_4': forms.TextInput(attrs={'class': 'form-control'}),
             'answer': forms.Select(attrs={'class': 'form-control'}),
             'mark': forms.NumberInput(attrs={'class': 'form-control'}),
             },
    extra=8, can_delete=True
)
