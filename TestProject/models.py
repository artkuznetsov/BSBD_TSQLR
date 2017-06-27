from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from datetime import *
from pytz import timezone

from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    GP = models.ForeignKey('GP', blank=True, null=True)

    def __str__(self):
        return self.username

    def get_group(self):
        return self.GP.__str__()


class New(models.Model):
    Title = models.CharField(max_length=50)
    Text = HTMLField()
    Date = models.DateTimeField(editable=False, default=datetime.now(timezone('Asia/Omsk')))
    Group = models.ManyToManyField('GP', blank=True, null=True)

    def __str__(self):
        return self.Title

    def get_text(self):
        return self.Text

    def get_date(self):
        return self.Date.date()

    def get_id(self):
        return self.id.__str__()


class GP(models.Model):
    NameGP = models.CharField(max_length=10)

    def __str__(self):
        return self.NameGP


class Category(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.Name


class Task(models.Model):
    NameTask = models.CharField(max_length=20)
    TaskText = models.TextField()
    WTask = models.TextField()
    Category = models.ManyToManyField('Category')
    Weight = models.IntegerField()
    ConnectDataBase = models.ForeignKey('ConnectDataBase')
    Vision = models.BooleanField()

    def __str__(self):
        return self.NameTask

    def get_tasktext(self):
        return self.TaskText

    def get_name(self):
        return self.NameTask

    def get_id(self):
        return self.id

    def get_weight(self):
        return self.Weight

    def get_connectdatabase(self):
        return self.ConnectDataBase

class DataBaseType(models.Model):
    Name = models.CharField(max_length=50)
    def __str__(self):
        return self.Name

class ConnectDataBase(models.Model):
    NameConnection = models.CharField(max_length=50)
    ConnectionString = models.TextField()
    ShadowConnectionString = models.TextField(default=None)
    Type = models.ForeignKey('DataBaseType')

    def __str__(self):
        return self.NameConnection

    def get_connection_string(self):
        return self.ConnectionString


class Test(models.Model):
    Name = models.CharField(max_length=30)
    DateActivate = models.DateTimeField()
    Time = models.IntegerField()
    Task = models.ManyToManyField('Task', through='TestTask')
    TestPerson = models.ManyToManyField('MyUser', through='TestPerson')

    def __str__(self):
        return self.Name

    def get_id(self):
        return self.id

    def get_time(self):
        return self.Time.__str__()


class TestConnectDataBase(models.Model):
    Test = models.ForeignKey('Test')
    ConnectDataBase = models.ForeignKey('ConnectDataBase')


class TestPerson(models.Model):
    Person = models.ForeignKey('MyUser')
    Test = models.ForeignKey(Test)
    Mark = models.FloatField(blank=True, null=True)
    StartTest = models.DateTimeField(blank=True, null=True)
    Variant = models.IntegerField()

    def get_mark(self):
        return self.Mark

    def get_mark_for_graphics(self):
        return int(self.Mark)

    def get_test(self):
        return self.Test

    def get_start_test(self):
        return self.StartTest

    def get_start_test_without_time(self):
        return self.StartTest.date()

    def get_start_test_dm(self):
        return str(str(self.StartTest.day) + '/' + str(self.StartTest.month))

    def get_variant(self):
        return self.Variant

    def get_person(self):
        return self.Person.username

    def get_person_all(self):
        return self.Person


class TestTask(models.Model):
    Test = models.ForeignKey('Test')
    Task = models.ForeignKey('Task')
    Variant = models.IntegerField()

    def get_task(self):
        return self.Task

    def get_test(self):
        return self.Test


class Answers(models.Model):
    TestTask = models.ForeignKey('TestTask')
    TestPerson = models.ForeignKey('TestPerson', default=None)
    Answer = models.TextField(max_length=30000)

    def get_answer(self):
        return self.Answer
