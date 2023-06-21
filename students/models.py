from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='Img/st_profile_img')
    address = models.CharField(max_length=60)
    mobile = models.CharField(max_length=20)

    @property
    def get_name(self):
        return self.user.first_name + ' ' + self.name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name
