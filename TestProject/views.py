# from django.http import HttpResponse
# from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe

from .forms import *
from .models import models
from django.http import *
from django.shortcuts import *
# from django.contrib.auth.models import User, Group
import random, json
from django.contrib.auth.decorators import login_required
import re
import pyodbc
from datetime import *
from pytz import timezone


def tests(request):
    if request.user.is_superuser:
        result = {}
        keys = []
        for group in GP.objects.all():
            students = MyUser.objects.filter(GP=group)
            result[group.NameGP] = students
        keys = ["username", "first_name", "last_name"]
        return render(request, 'TestProject/tests.html', {'students_list': result, 'keys': keys})


def home(request):
    return render(request, 'TestProject/home.html')


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
    return render(request, "TestProject/404.html")


@login_required(login_url='/accounts/login/')
def TestsUser(request):
    subscribe = TestPerson.objects.filter(Person=request.user.id)
    with_mark = []
    without_mark = []
    tz = timezone('Asia/Omsk')
    for sub in subscribe:
        if sub.get_mark() != None:
            with_mark.append(sub)
        else:
            if sub.Test.DateActivate <= datetime.now(tz):
                without_mark.append(sub)
    return render(request, "TestProject/profile.html",
                  {
                      "completed_tests": with_mark, "uncompleted_tests": without_mark
                  })


'''
def AddUsers(request):
    """Создание группы и пользоваетлей, которые входят в неё"""
    if request.user.is_superuser:
    	if request.method == ["POST"]:
    		Groups = request.POST['Group']
    		if Groups != "":
    			if GP.objects.get(NameGP = Groups) is None:
    				group = GP(NameGP=Groups)
    				group.save()
    				users = request.POST['users']
    				if users != '':
    					users = users.split('\n')
    					count = 0
    					for i in users:
    						user = i.split(' ')
    						person = MyUser.objects.create_user(
								username=Groups +"-"+ str(count),
	                            email=None,
	                            password='Qwerty123' + str(count),
	                            last_name=user[0],
	                            first_name=user[1],
	                            GP=group
	                       )
    						count += 1
    						person.save()
    					return redirect("/admin")
    				else:
    					return redirect("/admin")
    			else:
    				users = request.POST['users']
    				if users != '':
    					users = users.split('\n')
    					count = max(MyUser.objects.filter(GP = Groups))+1
    					for i in users:
    						user = i.split(' ')
    						person = MyUser.objects.create_user(
	                            username=Groups +"-"+ str(count),
	                            email=None,
	                            password='Qwerty123' + str(count),
	                            last_name=user[0],
	                            first_name=user[1],
	                            GP=group
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
'''
def AddUsers(request):
    """Создание группы и пользоваетлей, которые входят в неё"""
    if request.user.is_superuser:
    	if (request.method == "POST"):
    		Groups = request.POST['Group']
    		if Groups != "":
    			group = GP(NameGP=Groups)
    			group.save()
    			users = request.POST['users']
    			if users != '':
    				users = users.split('\n')
    				count = 0
    				for i in users:
    					user = i.split(' ')
    					person = MyUser.objects.create_user(
							username=Groups +"-"+ str(count),
	                        email=None,
	                        password='Qwerty123' + str(count),
	                        last_name=user[0],
	                        first_name=user[1],
	                        GP=group
	                    )
    					count += 1
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

            if (request.POST.get("check") == 'True'):
                """Get categories and count of tasks in him"""
                form = TestForm(request.POST)
                category = Category.objects.all()
                database = ConnectDataBase.objects.get(NameConnection=request.POST.get('ConnectDataBase'))
                tasks = Task.objects.filter(ConnectDataBase=database).values()

                di2 = []
                di = []
                for i in category:
                    di.append(str(i.id))
                    di.append(str(i))
                    di.append(len(tasks.filter(Category=i)))
                    di2.append(di)
                    di = []
                return JsonResponse({'status': 'ok', 'categories': di2, 'tasks': list(tasks)}, charset="utf-8",
                                    safe=True)

            else:
                data = json.loads(request.read().decode("utf-8"))
                database = ConnectDataBase.objects.get(NameConnection=data['ConnectDataBase'])
                task = Task.objects.filter(ConnectDataBase=database)
                category = Category.objects.all()

                answers = {}
                for i in re.findall(r'\d\d*', str(re.findall(r'categoryID\s\d\d*', str(data)))):
                    answers[i] = data['categoryID ' + i]

                test = Test(
                    Name=data['TestName'],
                    DateActivate=data['DateActivate'],
                    Time=data['Time']
                )
                test.save()

                connectDB = ConnectDataBase.objects.get(NameConnection=data['ConnectDataBase'])
                connectdatabase = TestConnectDataBase(Test=test, ConnectDataBase=connectDB)
                connectdatabase.save()

                for i in range(int(data['Variants'])):
                    for j in answers:
                        tasks = []
                        count = 0
                        t = []
                        for q in task.filter(Category=category.get(id=j)):
                            t.append(q.id)
                        r = [q for q in t]
                        while count != int(answers[j]):
                            RandomId = random.choice(r)
                            Check = RandomId in tasks
                            if Check == False:
                                tasks.append(RandomId)
                                test_task = TestTask.objects.create(Test=test, Task=task.get(id=RandomId),
                                                                    Variant=i + 1)
                                count += 1
                return JsonResponse({'status': 'ok'}, charset="utf-8", safe=True)

        else:
            form = TestForm()
            return render(request, 'admin/create_test.html', {'form': form})
    else:
        return redirect("/404")


def Add_TestPerson(request):
    """Привязка группы и(или) пользователя к тесту"""
    if request.user.is_superuser:
        if (request.method == "POST"):
            form = TestPersonForm(request.POST)
            if form.is_valid():

                Groups = form.cleaned_data['Group']
                Persons = form.cleaned_data['Person']
                test = form.cleaned_data['Test']
                testtask = TestTask.objects.filter(Test=test)
                students = []
                for i in Persons:
                    if i.GP in Groups:
                        continue
                    else:
                        students.append(i)

                for i in Groups:
                    students.extend(MyUser.objects.filter(GP=i))

                mas = []
                for i in testtask:
                    if i.Variant in mas:
                        continue
                    else:
                        mas.append(i.Variant)
                for st in students:
                    print(i)
                    tp = TestPerson.objects.filter(Person=st.id, Test=test)
                    print(tp)
                    tpv = [q.Variant for q in tp]
                    print(tpv)
                    t = [j for j in mas if ((j in tpv) == 0)]
                    print(t)
                    choise = random.choice(t)
                    testperson = TestPerson.objects.create(Person=st, Test=test, Variant=choise)
                return redirect("/admin")
        else:
            form = TestPersonForm()
            return render(request, 'admin/Add_TestPerson.html', {'form': form})
    else:
        return redirect("/404")


def GoTest(request, testid, var):
    if request.is_ajax():
        data = json.loads(request.read().decode("utf-8"))
        if len(data) == 1:
            # Здесь нужно обрабатывать запросы о проверки
            test = Test.objects.get(id=int(testid))
            connectdb = TestConnectDataBase.objects.get(Test=test)
            connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase).ConnectionString
            Connect = pyodbc.connect(connectStr)
            taskid = 0
            for i in data:
                taskid = int(i)
                curs = Connect.cursor()
                table = []
                try:
                    curs.execute(data[i])
                    l = [row for row in curs]
                    col = [column[0] for column in curs.description]
                    table.append(col)
                    a = []
                    for i in l:
                        for j in i:
                            a.append(j)
                        table.append(a)
                        a = []
                except Exception as exception:
                    result = re.search(r']\w[^(]*', str(exception)).group(0)[1::1]
                    dbname = re.search(r'\'\w*\.', result)
                    if dbname is not None:
                        result = result.replace(str(dbname.group(0)[1::1]), "")
                    if re.match(r'^You have an error in your SQL syntax', result) is not None:
                        fail = re.search(r'\'\w*[^\']*',result).group(0)
                        result = "<p>В вашем SQL запросе были найдены ошибки! </p><p>Проверьте правильность написания слов <div id=\"fail_text\">"+ fail + '\'</div></p>'
                    # table.append(error)
                    return JsonResponse({'status': 'error', 'error': result}, charset="utf-8", safe=True)
            return JsonResponse({'status': 'ok', 'table': table, 'task': taskid}, charset="utf-8", safe=True)
        else:
            test = Test.objects.get(id=int(testid))
            task = Task.objects.all()
            personForTest = TestPerson.objects.get(Person=request.user.id, Test=test, Variant=int(var))
            connectdb = TestConnectDataBase.objects.get(Test=test)
            connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase)
            Connect = pyodbc.connect(connectStr.ConnectionString)
            ConnectShadow = pyodbc.connect(connectStr.ShadowConnectionString)
            answ = 0
            weight = 0
            for i in data:
                temp = i.split(" ")[1]
                answer = Answers.objects.create(TestTask=TestTask.objects.get(Test=test,
                                                                              Task=Task.objects.get(id=temp),
                                                                              Variant=int(var)),
                                                TestPerson=personForTest, Answer=data[i])
                try:
                    curs = Connect.cursor()
                    curs.execute(data[i])
                    l = [row for row in curs]
                    curs = Connect.cursor()
                    curs.execute(str(task.get(id=int(temp)).WTask))
                    l1 = [row for row in curs]
                    Shadowcurs = ConnectShadow.cursor()
                    Shadowcurs.execute(data[i])
                    sl = [row for row in Shadowcurs]
                    Shadowcurs = ConnectShadow.cursor()
                    Shadowcurs.execute(str(task.get(id=int(temp)).WTask))
                    sl1 = [row for row in Shadowcurs]

                    if l1 == l and sl1 == sl:

                        answ += task.get(id=temp).Weight
                        weight += task.get(id=temp).Weight
                    else:

                        weight += task.get(id=temp).Weight
                except:

                    weight += task.get(id=temp).Weight

            personForTest.Mark = round(float(100 * answ / weight))
            personForTest.save()
            return JsonResponse({'status': 'ok'}, charset="utf-8", safe=True)

    else:
        tests = Test.objects.get(id=int(testid))
        task = Task.objects.all()
        connectdb = TestConnectDataBase.objects.get(Test=tests)
        connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase)
        Connect = pyodbc.connect(connectStr.ConnectionString)
        personForTest = TestPerson.objects.get(Person=request.user.id, Test=tests, Variant=int(var))
        tz = timezone('Asia/Omsk')
        if personForTest.Mark == None and tests.DateActivate <= datetime.now(tz):
            if (personForTest.StartTest == None):
                time = datetime.now(tz)
                personForTest.StartTest = time
                personForTest.save()
            else:
                time = personForTest.StartTest

            test = TestTask.objects.filter(Test=tests, Variant=int(var))
            table = []

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
                        a.append(str(k))
                    table.append(a)
                    a = []

                finalMonster[i.get_task().get_id()] = table

                table = []
            return render(request, "TestProject/test.html", {"GTest": test, "time": time, 'Monster': finalMonster})
        else:
            return redirect("/404")



def TakeAnswer(request):
    if request.user.is_superuser:
        if request.is_ajax():
            data = json.loads(request.read().decode("utf-8"))
            if data['GetTests'] == "True":
                tests = Test.objects.all()
                a = []
                for i in tests:
                    a.append(i.Name)
                return JsonResponse({'status': 'ok', 'tests': a}, charset="utf-8", safe=True)
            else:
                if data['GetStudents'] == "True":
                    test = Test.objects.get(Name=data['Test'])
                    students = {}
                    for i in TestPerson.objects.filter(Test=test):
                        for j in MyUser.objects.all():
                            if i.Person == j:
                                students[j.username] = 1
                    return JsonResponse({'status': 'ok', 'students': students}, charset="utf-8", safe=True)
                else:
                    if data['GetVariants'] == "True":
                        variants = {}
                        for i in TestPerson.objects.filter(Person=MyUser.objects.get(username=data['Student']),
                                                           Test=Test.objects.get(Name=data['Test'])):
                            variants[i.Variant] = 1
                        return JsonResponse({'status': 'ok', "variants": variants}, charset="utf-8", safe=True)
                    else:
                        if data['GetAnswers'] == "True":
                            test = Test.objects.get(Name=data['Test'])
                            student = MyUser.objects.get(username=data['Student'])
                            variant = data['Variant']
                            tt = TestTask.objects.filter(Test=test, Variant=variant)
                            tp = TestPerson.objects.get(Person=student, Test=test, Variant=variant)
                            answers = []
                            for i in tt:
                                tmp = []
                                tmp.append(i.Task.TaskText)
                                tmp.append(i.Task.WTask)
                                tmp.append(Answers.objects.get(TestTask=i, TestPerson=tp).get_answer())
                                answers.append(tmp)
                            return JsonResponse({'status': 'ok', "answers": answers}, charset="utf-8", safe=True)
        else:
            form = AnswerForm()
            return render(request, 'admin/answer_user.html', {'form': form})


def DeleteSubscribe(request):
    if request.user.is_superuser:
        if request.is_ajax():
            data = data = json.loads(request.read().decode("utf-8"))
            if data['GetGroups'] == "True":
                Groups = []
                tmp = GP.objects.all().values("NameGP")  # MyUser.objects.all().values("username")
                for i in tmp:
                    Groups.append(i['NameGP'])
                return JsonResponse({'status': 'ok', "groups": Groups}, charset="utf-8", safe=True)
            if data['GetResult'] == "True":
                student = MyUser.objects.filter(GP=GP.objects.get(NameGP=data['Group']))
                if data['Student'] != "False":
                    student = student.filter(username=data['Student'])
                mass = []
                for i in student:
                    tp = TestPerson.objects.all()
                    # tp = tp2
                    if data['Test'] != "False": tp = tp.filter(Test=Test.objects.get(Name=data['Test']))
                    if data['Mark'] != "False":

                        if data['Mark'] == 'null':
                            tp = tp.filter(Mark=None)
                        else:
                            tp = tp.filter(Mark=data['Mark'])
                    if data['Variant'] != "False": tp = tp.filter(Variant=data['Variant'])
                    mass.append(tp.filter(Person=MyUser.objects.get(username=i.username)))
                result = []
                for i in mass:
                    for j in i:
                        tmp = {}
                        tmp['Group'] = j.get_person_all().get_group()
                        tmp['Person'] = (j.get_person())
                        tmp['Test'] = (j.Test.Name)
                        tmp['Mark'] = (j.get_mark())
                        tmp['StartTest'] = (j.get_start_test())
                        tmp['Variant'] = (j.get_variant())
                        result.append(tmp)
                return JsonResponse({'status': 'ok', "result": result}, charset="utf-8", safe=True)
    return render(request, 'admin/delete_subscribe.html', {'answers': Answers.objects.all()})

@login_required(login_url='/accounts/login/')
def Trainer(request):
    if request.is_ajax():
        data = json.loads(request.read().decode("utf-8"))
        if data['start_test'] == "True":
            tasks = []
            for i in data['checked_categories']:
                subtasks = Task.objects.filter(Category=Category.objects.get(Name=i), Vision= True)
                if (subtasks.count() != 0):
                    for task in subtasks:
                        di = {}
                        table = []
                        Connect = pyodbc.connect(task.get_connectdatabase().ConnectionString)
                        curs = Connect.cursor()
                        curs.execute(task.WTask)
                        l = [row for row in curs]
                        col = [column[0] for column in curs.description]
                        table.append(col)
                        a = []
                        for j in l:
                            for k in j:
                                a.append(k)
                            table.append(a)
                            a = []

                        # finalMonster[i.get_task().get_id()] = table
                        di['id'] = task.id
                        di['name'] = task.NameTask
                        di['text'] = task.TaskText
                        di['table'] = table
                        table = []
                        tasks.append(di)
            return JsonResponse({'status': 'ok', 'tasks': tasks}, charset="utf-8", safe=True)
        if data['check_task'] == "True":
            task = Task.objects.get(id=int(data['id']))
            Connect = pyodbc.connect(task.ConnectDataBase.ConnectionString)
            curs = Connect.cursor()
            table = []
            try:
                curs.execute(data['user_query'])
                l = [row for row in curs]
                col = [column[0] for column in curs.description]
                table.append(col)
                a = []
                for i in l:
                    for j in i:
                        a.append(j)
                    table.append(a)
                    a = []
            except:
                table.append("error")
            return JsonResponse({'status': 'ok', 'table': table, 'task': task.id}, charset="utf-8", safe=True)
    categories = Category.objects.all()
    return render(request, 'TestProject/trainer.html', {'categories': categories})

def ShowUsers(request):
    if request.user.is_superuser:
        if request.is_ajax():
            data = json.loads(request.read().decode("utf-8"))
            if data['resetPassword'] == "True":
                a = MyUser.objects.get(id=data['user_id'])
                b = {}
                b['username'] = a.username
                b['email'] = a.email
                b['last_name'] = a.last_name
                b['first_name'] = a.first_name
                b['GP'] = a.GP
                a.delete()
                person = MyUser.objects.create_user(username=b['username'],
                                                    email=b['email'],
                                                    password="P@$$word",
                                                    GP=b['GP'])
                person.save()
                return JsonResponse({'status': 'ok'}, charset="utf-8", safe=True)

        result = []
        for group in GP.objects.all():
            for i in MyUser.objects.filter(GP=group):
                stud = []
                stud.append(i.id)
                stud.append(i.get_group())
                stud.append(i.username)
                stud.append(i.last_name)
                stud.append(i.first_name)
                result.append(stud)
        return render(request, 'admin/show_users.html', {'students_list': result})