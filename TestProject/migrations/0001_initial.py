# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('Answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('Name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ConnectDataBase',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('NameConnection', models.CharField(max_length=10)),
                ('ConnectionString', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GP',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('NameGP', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('NameTask', models.CharField(max_length=20)),
                ('TaskText', models.TextField()),
                ('WTask', models.TextField()),
                ('Weight', models.IntegerField()),
                ('Category', models.ForeignKey(to='TestProject.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('Name', models.CharField(max_length=30)),
                ('DateActivate', models.DateTimeField()),
                ('Time', models.IntegerField()),
                ('Variants', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TestConnectDataBase',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('ConnectDataBase', models.ForeignKey(to='TestProject.ConnectDataBase')),
                ('Test', models.ForeignKey(to='TestProject.Test')),
            ],
        ),
        migrations.CreateModel(
            name='TestPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('Mark', models.IntegerField(blank=True, null=True)),
                ('StartTest', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('Variant', models.IntegerField()),
                ('Task', models.ForeignKey(to='TestProject.Task')),
                ('Test', models.ForeignKey(to='TestProject.Test')),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(max_length=30, unique=True, error_messages={'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('GP', models.ForeignKey(null=True, to='TestProject.GP', blank=True)),
                ('groups', models.ManyToManyField(to='auth.Group', related_name='user_set', blank=True, related_query_name='user', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', related_name='user_set', blank=True, related_query_name='user', verbose_name='user permissions', help_text='Specific permissions for this user.')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='testperson',
            name='Person',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='testperson',
            name='Test',
            field=models.ForeignKey(to='TestProject.Test'),
        ),
        migrations.AddField(
            model_name='test',
            name='Task',
            field=models.ManyToManyField(through='TestProject.TestTask', to='TestProject.Task'),
        ),
        migrations.AddField(
            model_name='test',
            name='TestPerson',
            field=models.ManyToManyField(through='TestProject.TestPerson', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answers',
            name='TestTask',
            field=models.ForeignKey(to='TestProject.TestTask'),
        ),
    ]
