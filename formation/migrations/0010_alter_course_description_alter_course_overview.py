# Generated by Django 4.2.2 on 2023-06-12 20:37

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('formation', '0009_module_complet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='course',
            name='overview',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Overview'),
        ),
    ]