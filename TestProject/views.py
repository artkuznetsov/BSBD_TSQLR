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
import pyodbc


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
	if request.user.is_superuser:
		if request.is_ajax():
			data = json.loads(request.read().decode("utf-8"))
			task = Task.objects.all()
			category = Category.objects.all()

			#id_categories = re.findall(r'\d\d*', str(re.findall(r'categoryID\s\d\d*', str(data))))

			answers = {}
			for i in re.findall(r'\d\d*', str(re.findall(r'categoryID\s\d\d*', str(data)))):
				answers[i] = data['categoryID ' + i]

			# dic2 = {}
			# for i in data:
			# 	if len(i.split(' '))==2:
			# 		dic2[i.split(' ')[1]] =data[i]
			# print('dict2 = '+str(dic2))
			print('answers = '+str(answers))

			test = Test(
				Name = data['TestName'],
				DateActivate =data['DateActivate'],
				Time = data['Time']
			)
			test.save()

			connectDB = ConnectDataBase.objects.get(NameConnection = data['ConnectDateBase'])
			connectdatabase = TestConnectDataBase(Test = test, ConnectDataBase = connectDB)
			connectdatabase.save()

			for i in range(int(data['Variants'])):
				for j in answers:
					tasks = []
					count = 0
					t = []
					for q in task.filter(Category = category.get(id = j)):
						t.append(q.id)
					r = [q for q in t]
					while count!= int(answers[j]):
						RandomId = random.choice(r)
						Check = RandomId in tasks
						if Check == False:
							tasks.append(RandomId)
							test_task = TestTask.objects.create(Test = test, Task = task.get(id = RandomId),Variant=i+1)
							count+=1
			return JsonResponse({'status': 'ok'}, charset="utf-8", safe=True)
		else:
			form = TestForm()

			"""Get categories and count of tasks in him"""
			category = Category.objects.all()
			tasks = Task.objects.all()
			di = {}
			count = 0
			for i in category:
				di[len(tasks.filter(Category=i))] = i

			return render(request, 'admin/create_test.html', {'form': form,
															  'categoties': di
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
		if len(data) == 1:
			#Здесь нужно обрабатывать запросы о проверки
			return JsonResponse({'status': 'ok'}, charset="utf-8", safe=True)

		test = Test.objects.get(id=int(testid))
		task = Task.objects.all()
		personForTest = TestPerson.objects.get(Person = request.user.id, Test = test)
		connectdb = TestConnectDataBase.objects.get(Test = test)
		connectStr = ConnectDataBase.objects.get(NameConnection = connectdb.ConnectDataBase).ConnectionString
		Connect = pyodbc.connect(connectStr)
		answ = []
		for i in data:

			curs = Connect.cursor()
			curs1 = Connect.cursor()
			try:
				curs.execute(data[i])
				t = task.get(NameTask = i)
				curs1.execute(t.WTask)
				l = [row for row in curs]
				l1 = [row for row in curs1]
				if l1==l:
					answ.append(1)
				else:
					answ.append(0)
			except:
				answ.append(0)

		count = 0
		for i in answ:
			count +=i
		personForTest.Mark = int(count/len(answ))
		personForTest.save()



		return JsonResponse({'status': 'ok'}, charset="utf-8", safe=True)

	else:

		tests = Test.objects.get(id=int(testid))
		personForTest = TestPerson.objects.get(Person = request.user.id, Test = tests)
		time = timezone.now()
		personForTest.StartTest = time
		personForTest.save()

		test = TestTask.objects.filter(Test = tests	, Variant = personForTest.Variant)

		return render(request,"TestProject/test.html", {"GTest":test, "time":time})



