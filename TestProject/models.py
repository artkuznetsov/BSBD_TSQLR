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



class Task(models.Model):
	NameTask = models.CharField(max_length = 20)
	TaskText = models.TextField()
	WTask = models.TextField()
	Category = models.ForeignKey('Category')
	Weight = models.IntegerField()
	def __str__(self):
		return self.NameTask



class ConnectDataBase(models.Model):
	NameConnection = models.CharField(max_length = 10)
	ConnectionString = models.TextField()
	def __str__(self):
		return self.NameConnection

class Test(models.Model):
	Name = models.CharField(max_length = 30)
	DateActivate = models.DateTimeField()
	Time = models.IntegerField()
	Task = models.ManyToManyField('Task', through = 'TestTask')
	TestPerson = models.ManyToManyField('MyUser', through = 'TestPerson')
	Variants = models.IntegerField()
	def __str__(self):
		return self.Name

	def get_time(self):
		return self.Time.__str__()

class TestConnectDataBase(models.Model):
	Test = models.ForeignKey('Test')
	ConnectDataBase = models.ForeignKey('ConnectDataBase')		


class TestPerson(models.Model):
	Person = models.ForeignKey('MyUser')
	Test = models.ForeignKey(Test)
	Mark = models.IntegerField(blank = True, null = True)
	StartTest = models.DateTimeField()

	def get_mark(self):
		return self.Mark

	def get_test(self):
		return self.Test

	def get_start_test(self):
		return self.StartTest

class TestTask(models.Model):
	Test = models.ForeignKey('Test')
	Task = models.ForeignKey('Task')
	Variant = models.IntegerField()


class Answers(models.Model):
	TestTask = models.ForeignKey('TestTask')
	Answer = models.TextField()
