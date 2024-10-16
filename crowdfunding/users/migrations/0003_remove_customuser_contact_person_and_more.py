# Generated by Django 5.1 on 2024-10-16 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_contact_person_customuser_date_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='contact_person',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='organisation_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='project_id',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
