# Generated by Django 5.1 on 2024-12-01 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='organisation_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='organisation_contact',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='organisation_phone_number',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='organisation_ABN',
            field=models.CharField(max_length=11, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_charity',
            field=models.BooleanField(default=False),
        ),
    ]
