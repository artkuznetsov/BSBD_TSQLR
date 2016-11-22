# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import django.core.validators
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ConnectDataBase',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('NameConnection', models.CharField(max_length=10)),
                ('ConnectionString', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GP',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('NameGP', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Name', models.CharField(max_length=30)),
                ('DateActivate', models.DateTimeField()),
                ('Time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TestConnectDataBase',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('ConnectDataBase', models.ForeignKey(to='TestProject.ConnectDataBase')),
                ('Test', models.ForeignKey(to='TestProject.Test')),
            ],
        ),
        migrations.CreateModel(
            name='TestPerson',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Mark', models.IntegerField(null=True, blank=True)),
                ('StartTest', models.DateTimeField(null=True, blank=True)),
                ('Variant', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('Variant', models.IntegerField()),
                ('Task', models.ForeignKey(to='TestProject.Task')),
                ('Test', models.ForeignKey(to='TestProject.Test')),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('GP', models.ForeignKey(to='TestProject.GP', blank=True, null=True)),
                ('groups', models.ManyToManyField(to='auth.Group', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, related_query_name='user', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', related_name='user_set', help_text='Specific permissions for this user.', blank=True, related_query_name='user', verbose_name='user permissions')),
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
            field=models.ManyToManyField(to='TestProject.Task', through='TestProject.TestTask'),
        ),
        migrations.AddField(
            model_name='test',
            name='TestPerson',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='TestProject.TestPerson'),
        ),
        migrations.AddField(
            model_name='answers',
            name='TestTask',
            field=models.ForeignKey(to='TestProject.TestTask'),
        ),
    ]
