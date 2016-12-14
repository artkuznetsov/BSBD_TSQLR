from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
	GP = models.ForeignKey('GP', blank = True, null = True)

	def __str__(self):
		return self.username


class GP(models.Model):
	NameGP = models.CharField(max_length = 10)
	def __str__(self):
		return self.NameGP


class Category(models.Model):
	Name = models.CharField(max_length = 20)
	def __str__(self):
		return self.Name

	def get_id(self):
		return self.id


class Task(models.Model):
	NameTask = models.CharField(max_length = 20)
	TaskText = models.TextField()
	WTask = models.TextField()
	Category = models.ForeignKey('Category')
	Weight = models.IntegerField()
	ConnectDataBase = models.ForeignKey('ConnectDataBase')
	def __str__(self):
		return self.NameTask

	def get_tasktext(self):
		return self.TaskText

	def get_name(self):
		return self.NameTask

	def get_id(self):
		return self.id


class ConnectDataBase(models.Model):
	NameConnection = models.CharField(max_length = 10)
	ConnectionString = models.TextField()
	ShadowConnectionString = models.TextField(default = None)
	def __str__(self):
		return self.NameConnection


class Test(models.Model):
	Name = models.CharField(max_length = 30)
	DateActivate = models.DateTimeField()
	Time = models.IntegerField()
	Task = models.ManyToManyField('Task', through = 'TestTask')
	TestPerson = models.ManyToManyField('MyUser', through = 'TestPerson')

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
	Mark = models.FloatField(blank = True, null = True)
	StartTest = models.DateTimeField(blank = True, null = True)
	Variant = models.IntegerField()

	def get_mark(self):
		return self.Mark

	def get_test(self):
		return self.Test

	def get_start_test(self):
		return self.StartTest

	def get_start_test_without_time(self):
		return self.StartTest.date()

	def get_variant(self):
		return self.Variant


class TestTask(models.Model):
	Test = models.ForeignKey('Test')
	Task = models.ForeignKey('Task')
	Variant = models.IntegerField()

	def get_task(self):
		return self.Task

class Answers(models.Model):
	TestTask = models.ForeignKey('TestTask')
	TestPerson = models.ForeignKey('TestPerson', default = None)
	Answer = models.TextField()