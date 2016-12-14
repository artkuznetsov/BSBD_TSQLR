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

def tests(request):
	return render_to_response('TestProject/tests.html');

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
			if(request.POST['check']== True):
				"""Get categories and count of tasks in him"""
				form = TestForm(request.POST)
				category = Category.objects.all()

				tasks = Task.objects.filter(ConnectDataBase = form.cleaned_data['ConnectDateBase'])

				di = {}
				for i in category:
					di[i] = len(tasks.filter(Category=i))
				return JsonResponse({'status': 'ok', 'categoties':di, 'tasks':tasks}, charset="utf-8", safe=True)
			else:
				data = json.loads(request.read().decode("utf-8"))
				task = data['tasks']
				category = Category.objects.all()

				#id_categories = re.findall(r'\d\d*', str(re.findall(r'categoryID\s\d\d*', str(data))))

				answers = {}
				for i in re.findall(r'\d\d*', str(re.findall(r'categoryID\s\d\d*', str(data)))):
					answers[i] = data['categoryID ' + i]

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
			return render(request, 'admin/create_test.html', {'form': form})
	else:
		return redirect("/404")

def Add_TestPerson(request):
	"""Привязка группы и(или) пользователя к тесту"""
	if request.user.is_superuser:
		if(request.method=="POST"):
			form = TestPersonForm(request.POST)
			if form.is_valid():

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
					if i.Variant in mas :
						continue
					else:
						mas.append(i.Variant)
				for i in students:
					tp = TestPerson.objects.filter(Person = i, Test = test)
					tpv = [q.Variant for q in tp]
					t = [j for j in mas if((j in tpv)==0) ]
					choise = random.choice(t)
					testperson = TestPerson.objects.create(Person = i, Test = test, Variant = choise)
				return redirect("/admin")
		else:
			form = TestPersonForm()
			return render(request, 'admin/Add_TestPerson.html', {'form' : form})
	else:
		return redirect("/404")

def GoTest(request, testid, var):
	if request.is_ajax():
		data = json.loads(request.read().decode("utf-8"))
		if len(data) == 1:
			#Здесь нужно обрабатывать запросы о проверки
			test = Test.objects.get(id=int(testid))
			connectdb = TestConnectDataBase.objects.get(Test = test)
			connectStr = ConnectDataBase.objects.get(NameConnection = connectdb.ConnectDataBase).ConnectionString
			Connect = pyodbc.connect(connectStr)
			taskid = 0
			for i in data:
				taskid = int(i)
				curs = Connect.cursor()
				table = []
				try:
					curs.execute(data[i])
					l = [row for row in curs]
					print('l = ' + str(l))
					col = [column[0] for column in curs.description]
					table.append(col)
					a = []
					for i in l:
						for j in i:
							a.append(j)
						table.append(a)
						a=[]
				except:
					table['error'] = 'error'
			print(table)
			return JsonResponse({'status': 'ok', 'table': table,'task': taskid}, charset="utf-8", safe=True)
		else:
			test = Test.objects.get(id=int(testid))
			task = Task.objects.all()
			personForTest = TestPerson.objects.get(Person=request.user.id, Test=test, Variant=int(var))
			connectdb = TestConnectDataBase.objects.get(Test=test)
			connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase)
			Connect = pyodbc.connect(connectStr.ConnectionString)
			ConnectShadow = pyodbc.connect(connectStr.ShadowConnectionString)
			answ = []
			weight = 0
			for i in data:
				temp = i.split(" ")[1]
				answer = Answers.objects.create(TestTask=TestTask.objects.get(Task=task.get(id=temp), Test=test),
												TestPerson=personForTest, Answer=data[i])
				curs = Connect.cursor()
				curs1 = Connect.cursor()
				Shadowcurs = ConnectShadow.cursor()
				Shadowcurs1 = ConnectShadow.cursor()
				try:
					Shadowcurs.execute(data[i])
					curs.execute(data[i])

					curs1.execute(task.get(id=temp).WTask)
					Shadowcurs1.execute(task.get(id=temp).WTask)
					l = [row for row in curs]
					l1 = [row for row in curs1]
					sl = [row for row in Shadowcurs]
					sl1 = [row for row in Shadowcurs1]
					if l1 == l and sl1 == sl:
						answ.append(task.get(id=temp).Weight)
						weight += task.get(id=temp).Weight
					else:
						answ.append(0)
						weight += task.get(id=temp).Weight
				except:
					answ.append(0)
					weight += task.get(id=temp).Weight

			count = 0
			for i in answ:
				count += i
			personForTest.Mark = 100 * count / weight
			personForTest.save()
			return JsonResponse({'status': 'ok'}, charset="utf-8", safe=True)

	else:

		tests = Test.objects.get(id=int(testid))
		task = Task.objects.all()
		connectdb = TestConnectDataBase.objects.get(Test=tests)
		connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase)
		Connect = pyodbc.connect(connectStr.ConnectionString)
		personForTest = TestPerson.objects.get(Person=request.user.id, Test=tests, Variant=int(var))

		if (personForTest.StartTest == None):
			time = timezone.now()
			personForTest.StartTest = time
			personForTest.save()
		else:
			time = personForTest.StartTest

		test = TestTask.objects.filter(Test=tests, Variant=int(var))
		table = []
		# print(test)
		finalMonster = {}
		for i in test:
			curs = Connect.cursor()
			curs.execute(i.get_task().WTask)
			l = [row for row in curs]
			col = [column[0] for column in curs.description]
			table.append(col)
			a = []
			for j in l:
				for k in j:
					a.append(k)
				table.append(a)
				a = []
			# print('table = '+ str(table))
			finalMonster[i.get_task().get_id()] = table
			# print('finalMonster = '+ str(finalMonster))
			table=[]
		return render(request,"TestProject/test.html", {"GTest":test, "time":time, 'Monster':finalMonster})

def TakeAnswer(request):
	if request.user.is_superuser:
		if (request.method == "POST"):
			form = 	AnswerForm(request.POST)
			if form.is_valid():
				test = form.cleaned_data["Test"]
				person = form.cleaned_data["Person"]
				variant = form.cleaned_data["Variant"]
				testperson = TestPerson.objects.get(Person = person, Test = test, Variant = variant)
				testtask = TestTask.objects.filter(Test = test, Variant = testperson.Variant)
				answers = []
				for i in testtask:
					answers.append(Answers.objects.get(TestPerson = testperson, TestTask = i))
				return render(request, 'TestProject/answer_user.html', {'answers': answers})
		else:
			form = AnswerForm()
			return render(request, 'admin/answer.html', {'form' : form})

