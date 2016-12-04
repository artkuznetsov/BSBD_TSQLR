#from django.http import HttpResponse
#from django.shortcuts import render_to_response
from .forms import *
from .models import models
from django.http import *
from django.shortcuts import *
#from django.contrib.auth.models import User, Group
import random, json
from django.contrib.auth.decorators import login_required
import re



def home(request):
    return render_to_response('TestProject/home.html')

def register(request):
    return render_to_response('registration/registration_form.html')

def login_page(request):
    return render_to_response('registration/login.html')

def logout_page(request):
    return render_to_response('registration/logout.html')

def registration_closed(request):
    return render_to_response('registration/registration_closed.html')

def registration_complete(request):
    return render_to_response('registration/registration_complete.html')


def error404(request):
	return render(request,"TestProject/404.html")




@login_required(login_url='/accounts/login/')
def TestsUser(request):
	subscribe = TestPerson.objects.filter(Person = request.user.id)
	with_mark = []
	without_mark = []
	for sub in subscribe:
		if sub.get_mark() != None:
			with_mark.append(sub)
		else:
			without_mark.append(sub)
	return render(request,"TestProject/profile.html",
                  {
					  "completed_tests":with_mark, "uncompleted_tests":without_mark
                  })

def AddUsers(request):
	"""Создание группы и пользоваетлей, которые входят в неё"""
	if request.user.is_superuser:
		if (request.method == "POST"):
			Groups = request.POST['Group']
			if Groups != "":
				group = GP(NameGP = Groups)
				group.save()
				users = request.POST['users']
				if users != '':
					users = users.split('\n')
					count = 0
					for i in users:

						user = i.split(' ')

						person =MyUser.objects.create_user(
							username = Groups + str(count),
							email =None,
							password = 'Qwerty123'+ str(count),
							last_name = user[0],
							first_name = user[1],
							GP = group
						)
						count+=1
						person.save()
					return redirect("/admin")
				else:
					return redirect("/admin")
			else:
				return redirect("/admin")	
		else:
			return render(request, "admin/generate_users.html")
	else:
		return redirect("/404")


def CreateTest(request):
	"""Cоздание теста с вариантами"""
	if request.is_ajax():
		data = json.loads(request.read().decode("utf-8"))
		dict = {}
		for i in data:
			dict[i] = data[i]
		"""Для примера выведем ответа на 9 таск"""
		#print(dict['categoryID 5'])
		return JsonResponse({'status':'ok'}, charset="utf-8",safe=True)

	if request.user.is_superuser:
		if (request.method == "POST"):
			form = TestForm(request.POST)
			task = Task.objects.all()
			category = Category.objects.all()
			taskId = []
			taskC = []
			for i in range(len(category)):
				for j in task.filter(Category = category[i]):
					taskC.append(j.id)
				taskId.append(taskC)
			if form.is_valid():
				test = Test(
					Name = form.cleaned_data['Name'],
					DateActivate =form.cleaned_data['DateActivate'],
					Time = form.cleaned_data['Time']
				)
				test.save()
				connectdatabase = TestConnectDataBase(Test = test, ConnectDataBase = form.cleaned_data['ConnectDataBase'])
				connectdatabase.save()
				for i in range(form.cleaned_data['Variants']):
					for j in range(len(category)):
						tasks = []
						count = 0
						while count!= int(request.POST['input'+str(j+1)]):
							RandomId = random.choice(taskId[j])
							Check = RandomId in tasks
							if Check == False:
								tasks.append(RandomId)
								test_task = TestTask.objects.create(Test = test, Task = task.get(id = RandomId),Variant=i+1)
								count+=1
				return redirect("/admin")
		else:
			form = TestForm()

			"""Get categories and count of tasks in him"""
			category = Category.objects.all()
			tasks = Task.objects.all()
			dict = {}
			count = 0
			for i in category:
				dict[len(tasks.filter(Category=i))] = i

			return render(request, 'admin/create_test.html', {'form': form,
															  'categoties': dict
														  })
	else:
		return redirect("/404")

def Add_TestPerson(request):
	"""Привязка группы и(или) пользователя к тесту"""
	if request.user.is_superuser:
		if(request.method=="POST"):
			form = TestPersonForm(request.POST)
			if form.is_valid():
				max = 0

				Groups = form.cleaned_data['Group']
				Persons = form.cleaned_data['Person']
				test = form.cleaned_data['Test']
				testtask =  TestTask.objects.filter(Test = test)
				students = []
				for i in Persons:
					if i.GP in Groups:
						continue
					else:
						students.append(i)

				for i in Groups:
					students.extend(MyUser.objects.filter(GP = i))

				mas = []
				for i in testtask:
					if i.Variant in mas:
						continue
					else:
						mas.append(i.Variant)

				for i in students:
					choise = random.choice(mas)
					testperson = TestPerson.objects.create(Person = i, Test = test, Variant = choise)
				return redirect("/admin")
		else:
			form = TestPersonForm()
			return render(request, 'admin/Add_TestPerson.html', {'form' : form})
	else:
		return redirect("/404")

def GoTest(request, testid):
	if request.is_ajax():
		data = json.loads(request.read().decode("utf-8"))
		dict= {}
		for i in data:
			dict[i] = data[i]
		"""Для примера выведем ответа на 9 таск"""
		print(dict['taskID 9'])

	personForTest = TestPerson.objects.get(Person = request.user.id)
	tests = Test.objects.get(id=int(testid))
	test = TestTask.objects.filter(Test = tests	, Variant = personForTest.Variant)

	return render(request,"TestProject/test.html", {"GTest":test})



