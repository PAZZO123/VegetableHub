# Generated by Django 5.1.3 on 2024-11-28 13:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webapp', '0002_application_created_at_alter_application_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Names', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\+?\\d{10,15}$', message='Enter a valid phone number.')])),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]