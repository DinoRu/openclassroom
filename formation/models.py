from django.db import models
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.


class Subject(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Course(models.Model):
    LEVEL = (
        ('EASY', 'Easy'),
        ('MEDIUM', 'Medium'),
        ('HARD', 'Hard'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    overview = CKEditor5Field('Overview', config_name='extends')
    description = CKEditor5Field('Description', config_name='extends')
    thumbnail = models.ImageField(
        upload_to='Course_img/', null=True, blank=True)
    thumbnail_url = models.URLField(max_length=600, null=True, blank=True)
    level = models.CharField(max_length=20, choices=LEVEL)
    learn_hours = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    students = models.ManyToManyField(
        User, related_name='formation_joined', blank=True)
    total_score = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=600)
    slug = models.SlugField(null=True, blank=True)
    overview = models.TextField()
    complet = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']


class Content(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name='contents')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': (''
                                                                                                            'text',
                                                                                                            'file',
                                                                                                            'image',
                                                                                                            'video'
                                                                                                            )})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['object_id', 'pk']


class ItemBase(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)s_related')
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f'formation/content/{self._meta.model_name}.html', {'item': self}
        )


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(max_length=600, upload_to='Img/course_files')


class Image(ItemBase):
    image = models.ImageField(upload_to='Img/course_im')


class Video(ItemBase):
    url = models.URLField()


class Question(models.Model):

    OPTION_CHOICE = (
        ('Option_1', 'Option_1'),
        ('Option_2', 'Option_2'),
        ('Option_3', 'Option_3'),
        ('Option_4', 'Option_4'),
    )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='questions')
    mark = models.PositiveIntegerField()
    question = models.CharField(max_length=1000)
    option_1 = models.CharField(max_length=1000)
    option_2 = models.CharField(max_length=1000)
    option_3 = models.CharField(max_length=1000)
    option_4 = models.CharField(max_length=1000)
    answer = models.CharField(max_length=20, choices=OPTION_CHOICE)

    def __str__(self):
        return self.question


class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='results')
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exam.title
