# Generated by Django 4.2.2 on 2023-06-11 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formation', '0008_alter_module_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='complet',
            field=models.BooleanField(default=False),
        ),
    ]