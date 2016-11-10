from django.db import models
from django.utils import timezone


class Category(models.Model):
	Name = models.CharField(max_length = 20)
	def __str__(self):
		return self.NameClass

class Students(models.Model):
	NameGroup = models.CharField(max_length = 10)
	Person = models.ForeignKey('auth.User')
	def __str__(self):
		return self.NameGroup



class Task(models.Model):
	NameTask = models.CharField(max_length = 20)
	TaskText = models.TextField()
	WTask = models.TextField()
	Category = models.ForeignKey('Category')
	Weight = models.IntegerField()
	def __str__(self):
		return self.NameQuest



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
	TestPerson = models.ManyToManyField('auth.User', through = 'TestPerson')
	Variants = models.IntegerField()
	def __str__(self):
		return self.Name

	def get_time(self):
		return self.Time.__str__()

class TestConnectDataBase(models.Model):
	Test = models.ForeignKey('Test')
	ConnectDataBase = models.ForeignKey('ConnectDataBase')		


class TestPerson(models.Model):
	Person = models.ForeignKey('auth.User')
	Test = models.ForeignKey(Test)
	Mark = models.IntegerField(blank = True)
	StartTest = models.DateTimeField()


class TestTask(models.Model):
	Test = models.ForeignKey('Test')
	Task = models.ForeignKey('Task')
	Variant = models.IntegerField()


class Answers(models.Model):
	TestTask = models.ForeignKey('TestTask')
	Answer = models.TextField()
