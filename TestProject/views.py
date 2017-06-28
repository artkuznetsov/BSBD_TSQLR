# from django.http import HttpResponse
# from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.contrib.auth.models import *

from PIL import Image
from wsgiref.util import FileWrapper
from TestApp import settings
from .forms import *
from .models import models
from django.http import *
from django.shortcuts import *
from django.http import FileResponse
# from django.contrib.auth.models import User, Group
import random, json
from django.contrib.auth.decorators import login_required
import re
import pyodbc
from datetime import *
from pytz import timezone
import eralchemy
from eralchemy import render_er
import base64
import hashlib
from django.db.models import Q
import psycopg2

def get_news(user):
    news_array = []
    try:
        for i in New.objects.filter(Q(Group=GP.objects.get(id=user.GP.id)) | Q(Group__isnull=True)):
            news_array.append(i)
    except:
        news_array = []
    return news_array


@login_required(login_url='/accounts/login/')
def News(request, newid):
    new_required = New.objects.get(id=newid)
    for new in get_news(MyUser.objects.get(id=request.user.id)):
        if new_required == new:
            return render(request, "TestProject/new.html", {'new': new})
    return redirect("/404")



@login_required(login_url='/accounts/login/')
def tests(request):
    if request.is_ajax():
        data = json.loads(request.read().decode("utf-8"))
        user = MyUser.objects.get(id=request.user.id)
        user.set_password(data['Password'])
        user.save()
        return JsonResponse({'status': 'ok'}, charset="utf-8", safe=True)
    else:
        subscribe = TestPerson.objects.filter(Person=request.user.id).order_by('Test__DateActivate')
        user = MyUser.objects.get(id=request.user.id)

        with_mark = []
        without_mark = []
        tz = timezone('Asia/Omsk')
        for sub in subscribe:
            if sub.get_mark() != None:
                with_mark.append(sub)
            else:
                if sub.Test.DateActivate <= datetime.now(tz):
                    without_mark.append(sub)

        return render(request, "TestProject/base-2.html",
                      {
                          "completed_tests": with_mark,
                          "uncompleted_tests": without_mark,
                          "news": get_news(user)
                      })
        # return render(request,'TestProject/base-2.html')


@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, 'TestProject/home.html')


@login_required(login_url='/accounts/login/')
def some_test(request, testid, var):
    if request.is_ajax():
        # Проверка студентом написанного запроса
        data = json.loads(request.read().decode("utf-8"))
        if len(data) == 1:
            # Здесь нужно обрабатывать запросы о проверке ...
            test = Test.objects.get(id=int(testid))
            personForTest = TestPerson.objects.get(Person=request.user.id, Test=test, Variant=int(var))
            connectdb = TestConnectDataBase.objects.get(Test=test)
            connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase).ConnectionString
            database_type = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase).Type
            for i in data:
                # ... или получении схемы БД
                if data[i] == 'GetDBSchema':
                    if database_type.Name == 'MySQL':
                        host = re.search(r'\w*SERVER=\w*', connectStr).group(0)[7:]
                        user = re.search(r'\w*UID=\w*', connectStr).group(0)[4:]
                        password = re.search(r'\w*PWD=\w*', connectStr).group(0)[4:]
                        database = re.search(r'\w*DATABASE=\w*', connectStr).group(0)[9:]
                        render_er('mysql+pymysql://' + user + ':' + password + '@' + host + '/' + database + '','' + host + '->' + database + '.png')
                        response = base64.b64encode(open(host + '->' + database + '.png',"rb").read())
                        return JsonResponse({'status':'ok', 'image':str(response)},safe=True)
                    if database_type.Name == 'PostgreSQL':
                        #lines = [line.rstrip('\n') for line in open('/etc/odbc.ini')]
                        #dsn_name = re.search(r'\w*DSN=\w*', connectStr).group(0)[4:]
                        #print('DSN_NAME IS ' + dsn_name)
                        Connect = psycopg2.connect(connectStr)
                        print(Connect)
                        host = re.search(r'\w*host=\w*',connectStr).group(0)[5:]
                        print(host)
                        user = re.search(r'\w*user=\w*',connectStr).group(0)[5:]
                        print(user)
                        database = re.search(r'\w*dbname=\w*',connectStr).group(0)[7:]
                        print(database)
                        password = re.search(r'\w*password=\w*',connectStr).group(0)[9:]
                        print(password)
                        render_er('postgresql+psycopg2://' + str(user) + ':' + str(password) + '@' + str(host) + '/' + str(database) + '','' + str(host) + '->' + str(database) + '.png')    
                        response = base64.b64encode(open(host + '->' + database + '.png', "rb").read())
                        return JsonResponse({'status': 'ok', 'image': str(response)}, safe=True)

            Connect = 1
            try:
                test_connect = pyodbc.connect(connectStr)
                Connect = test_connect
            except:
                test_connect = psycopg2.connect(connectStr)
                Connect = test_connect
            taskid = 0
            for i in data:
                taskid = int(i)
                try:
                    ans = Answers.objects.get(TestPerson=personForTest,
                                              TestTask=TestTask.objects.get(Task=Task.objects.get(id=taskid),
                                                                            Test=test, 
                                                                            Variant=var))
                    ans.Answer = data[i]
                    ans.RightCheck = False
                    ans.save()
                except:
                    ans = Answers.objects.create(TestPerson=personForTest,
                                                 TestTask=TestTask.objects.get(Task=Task.objects.get(id=taskid),
                                                                               Test=test, 
                                                                               Variant=var),
                                                 Answer=data[i])
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
                        fail = re.search(r'\'\w*[^\']*', result).group(0)
                        result = "<p>В вашем SQL запросе были найдены ошибки! </p><p>Проверьте правильность написания слов <div id=\"fail_text\">" + fail + '\'</div></p>'
                    return JsonResponse({'status': 'error', 'error': result}, charset="utf-8", safe=True)
            return JsonResponse({'status': 'ok', 'table': table, 'task': taskid}, charset="utf-8", safe=True)
        else:
            # Проверка ответов студента и их сохранение в базу, после нажатия на кнопку завершения
            test = Test.objects.get(id=int(testid))
            task = Task.objects.all()
            personForTest = TestPerson.objects.get(Person=request.user.id, Test=test, Variant=int(var))
            connectdb = TestConnectDataBase.objects.get(Test=test)
            connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase)
            ConnectShadow = 1
            Connect = 1
            with_exception = False
            db_type = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase).Type
            if db_type.Name == 'MySQL':
                print('try to connect via PYDOBC')
                Connect = pyodbc.connect(connectStr.ConnectionString)
                print('Connect = ')
                print(Connect)
                ConnectShadow = pyodbc.connect(connectStr.ShadowConnectionString)
                print('ConnectShadow = ')
                print(ConnectShadow)
            if db_type.Name == 'PostgreSQL':
                print('try to connect via PSYCOPG2')
                Connect = psycopg2.connect(connectStr.ConnectionString)
                print('Connect = ')
                print(Connect)
                ConnectShadow = psycopg2.connect(connectStr.ShadowConnectionString)
                print('ConnectShadow = ')
                print(ConnectShadow)
            answ = 0
            weight = 0
            if test.HardCheck == 0:
                print('HardCheck = False')
                for i in data:
                    temp = i.split(" ")[1]
                    if temp == "Test":
                        continue
                    else:
                        try:
                            ans = Answers.objects.get(TestPerson=personForTest,
                                                  TestTask=TestTask.objects.get(Task=Task.objects.get(id=temp), Test=test,
                                                                                Variant=var))
                            ans.Answer = data[i]
                            ans.RightCheck = False
                            ans.save()
                        except Exception as e:
                            print(e)
                            ans = Answers.objects.create(TestPerson=personForTest,
                                                     TestTask=TestTask.objects.get(Task=Task.objects.get(id=temp),
                                                                                   Test=test, Variant=var),
                                                     Answer=data[i], RightCheck = False)
                        try:
                        #print('data = ')
                        #print(data)
                            curs = Connect.cursor()
                        #print('curs = ')
                        #print(curs)
                        #print('data[i] = ')
                        #print(data[i])
                            curs.execute(data[i])
                            l = [row for row in curs]
                        #print('l = ')
                        #print(l)
                            curs = Connect.cursor()
                            curs.execute(str(task.get(id=int(temp)).WTask))
                            l1 = [row for row in curs]
                        #print('l1= ')
                        #print(l1)
                            Shadowcurs = ConnectShadow.cursor()
                            Shadowcurs.execute(data[i])
                            sl = [row for row in Shadowcurs]
                        #print('sl = ')
                        #print(sl)
                            Shadowcurs = ConnectShadow.cursor()
                            Shadowcurs.execute(str(task.get(id=int(temp)).WTask))
                            sl1 = [row for row in Shadowcurs]
                        #print('sl1 = ')
                        #print (sl1)
                            if l1 == l and sl1 == sl:
                            #print('l1 == l and sl1 == sl')
                                answ += task.get(id=temp).Weight
                            #print('answ = ')
                            #print(answ)
                                answer_right = Answers.objects.get(TestPerson=personForTest, TestTask=TestTask.objects.get(Task=Task.objects.get(id=temp), Test=test, Variant=var), Answer=data[i])
                                print(answer_right)
                                answer_right.RightCheck = True
                                print(answer_right)
                                answer_right.save()
                                weight += task.get(id=temp).Weight
                            #print('weight = ')
                            #print(weight)
                            else:
                            #print('ELSE FOR l1 == l and sl1 == sl')
                                weight += task.get(id=temp).Weight
                            #print('weight = ')
                            #print(weight)
                        except Exception as e:
                            print(e)
                        #print('exception!!!!!!')
                            weight += task.get(id=temp).Weight
                            with_exception = True
                        #print('weight = ')
                        #print(weight)
            else:
                print('Hardcheck = True')
                for i in data:
                    temp = i.split(" ")[1]
                    if temp == "Test":
                        continue
                    else:
                        try:
                            ans = Answers.objects.get(TestPerson = personForTest, TestTask = TestTask.objects.get(Task = Task.objects.get(id=temp), Test = test, Variant = var))
                            print(ans)
                            ans.Answer = data[i]
                            ans.RightCheck = False
                            print(ans.Answer)
                            ans.save()
                            print('this shit has been saved')
                        except Exception as e:
                            print(e)
                            ans = Answers.objects.create(TestPerson = personForTest, TestTask = TestTask.objects.get(Task=Task.objects.get(id=temp),Test=test, Variant=var), Answer=data[i], RightCheck = False)
                        try:
                            l=[]
                            l1=[]
                            sl=[]
                            sl1=[]

                            curs = Connect.cursor()
                            curs.execute(data[i])
                            l = [row for row in curs]
                            column_name = [row[0] for row in curs.description]
                            print('column_name')
                            print(column_name)
                            curs1 = Connect.cursor()
                            print('curs1')
                            print(curs1)
                            curs1.execute(str(task.get(id=int(temp)).WTask))
                            print('curs1.execute(WTask)')
                            print(curs1.execute(str(task.get(id=int(temp)).WTask)))
                            l1 = [row for row in curs1]
                            column_name_w = [row[0] for row in curs1.description]
                            print('column_name_w')
                            print(column_name_w)
                            Shadowcurs = Connect.cursor()
                            Shadowcurs.execute(data[i])
                            sl = [row for row in Shadowcurs]
                            column_name_shadow = [row[0] for row in Shadowcurs.description]
                            print('column_name_shadow')
                            print(column_name_shadow)
                            Shadowcurs1 = Connect.cursor()
                            Shadowcurs1.execute(str(task.get(id=int(temp)).WTask))
                            sl1 = [row for row in Shadowcurs1]
                            column_name_w_shadow = [row[0] for row in Shadowcurs1.description]
                            print('column_name_w_shadow')
                            print(column_name_w_shadow)
                            dic_check_student_light_table = {}
                            dic_check_student_shadow_table = {}
                            dic_check_teacher_light_table = {}
                            dic_check_teacher_shadow_table = {}

                            for j in range(len(column_name)):
                                dic_check_student_light_table[column_name[j]] = [row[j] for row in l]

                            for j in range(len(column_name_shadow)):
                                dic_check_student_shadow_table[column_name_shadow[j]] = [row[j] for row in sl]

                            for j in range(len(column_name_w)):
                                dic_check_teacher_light_table[column_name_w[j]] = [row[j] for row in l1]

                            for j in range(len(column_name_w_shadow)):
                                dic_check_teacher_shadow_table[column_name_w_shadow[j]] = [row[j] for row in sl1]


                            if dic_check_student_shadow_table == dic_check_teacher_shadow_table and dic_check_student_shadow_table == dic_check_teacher_shadow_table:
                                answ += task.get(id=temp).Weight
                                right_check = Answers.objects.get(TestPerson=personForTest, TestTask = TestTask.objects.get(Task=Task.objects.get(id=temp), Test=test, Variant=var), Answer=data[i])
                                right_check.RightCheck = True
                                right_check.save()
                                weight += task.get(id=temp).Weight
                            else:
                                weight += task.get(id=temp).Weight
                        except Exception as e:
                            print('Im here!!!')
                            print(e)
                            weight += task.get(id=temp).Weight

            personForTest.Mark = round(float(100 * answ / weight))
            #print('personForTest.Mark = ')
            #print(personForTest.Mark)
            personForTest.save()
            return JsonResponse({'status': 'ok', 'except': with_exception}, charset="utf-8", safe=True)

    else:
        # Формирование страниц для теста
        # Определение теста, студента, который проходит тест
        tests = Test.objects.get(id=int(testid))
        task = Task.objects.all()
        connectdb = TestConnectDataBase.objects.get(Test=tests)
        connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase)
        Connect = 1
        try:
            test_connect = psycopg2.connect(connectStr.ConnectionString)
            Connect = test_connect
        except:
            test_connect = pyodbc.connect(connectStr.ConnectionString)
            Connect = test_connect

        personForTest = TestPerson.objects.get(Person=request.user.id, Test=tests, Variant=int(var))
        test = TestTask.objects.filter(Test=tests, Variant=int(var))
        CheckAnswer = False
        # Проверка наличия ответов на этот тест
        for q in test:
            if len(Answers.objects.filter(TestPerson=personForTest, TestTask=q)) == 0:
                CheckAnswer = False
            else:
                CheckAnswer = True
                continue
                # Запуск таймера
        tz = timezone('Asia/Omsk')
        if personForTest.Mark == None and tests.DateActivate <= datetime.now(tz):
            if (personForTest.StartTest == None):
                time = datetime.now(tz)
                personForTest.StartTest = time
                personForTest.save()
            else:
                time = personForTest.StartTest
            # Если ответов нет, то отдаётся страница с пустыми полями для заполнения


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
            if CheckAnswer == False:
                return render(request, "TestProject/tests.html", {"GTest": test, "time": time, 'Monster': finalMonster})
            else:
                answers = {}
                # for w in test:
                # answers[w.get_task().get_id()] = Answers.objects.get(TestPerson=personForTest,
                #                                                      TestTask=w).get_answer()
                return render(request, "TestProject/tests.html",
                              {"GTest": test,
                               "time": time,
                               'Monster': finalMonster,
                               "answers": answers})
        else:
            return redirect("/404")


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
    return render(request, "TestProject/base-2.html",
                  {
                      "completed_tests": with_mark, "uncompleted_tests": without_mark
                  })


'''
def AddUsers(request):
    """Создание группы и пользоваетлей, которые входят в неё"""
    if request.user.is_superuser:

        if request.method == ["POST"]:
            print('y')
            Groups = request.POST['Group']
            if Groups != "":
                if len(GP.objects.filter(NameGP = Groups))  == 0:
                    print('1')
                    group = GP(NameGP=Groups)
                    group.save()
                    users = request.POST['users']
                    if users != '':
                        print('2')
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
                    print('3')
                    users = request.POST['users']
                    if users != '':
                        users = users.split('\n')
                        count = max(MyUser.objects.filter(GP = Groups))+1
                        print(count)
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
                        print('haha')
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
                            username=Groups + "-" + str(count),
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
    global date_activate
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
                    Time=data['Time'],
                    HardCheck=data['HardCheck']
                )
                test.save()

                connectDB = ConnectDataBase.objects.get(NameConnection=data['ConnectDataBase'])
                connectdatabase = TestConnectDataBase(Test=test, ConnectDataBase=connectDB)
                connectdatabase.save()

                for i in range(int(data['Variants'])):
                    tasks = []
                    for j in answers:
                        count = 0
                        t = []
                        for q in task.filter(Category=category.get(id=j)):
                            t.append(q.id)
                        r = [q for q in t]
                        testlist = [w for w in r if w not in tasks]
                        if len(testlist) >= int(answers[j]):
                            while count != int(answers[j]):
                                RandomId = random.choice(r)
                                Check = RandomId in tasks
                                if Check == False:
                                    tasks.append(RandomId)
                                    test_task = TestTask.objects.create(Test=test, Task=task.get(id=RandomId),
                                                                        Variant=i + 1)
                                    count += 1
                        else:
                            Test.objects.filter(Name=data['TestName']).delete()
                            return JsonResponse({'status': 'error'}, charset="utf-8", safe=True)
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
        # Проверка студентом написанного запроса
        data = json.loads(request.read().decode("utf-8"))
        if len(data) == 1:
            # Здесь нужно обрабатывать запросы о проверке ...
            test = Test.objects.get(id=int(testid))
            personForTest = TestPerson.objects.get(Person=request.user.id, Test=test, Variant=int(var))
            connectdb = TestConnectDataBase.objects.get(Test=test)
            connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase).ConnectionString
            for i in data:
                # ... или получении схемы БД
                if data[i] == 'GetDBSchema':
                    host = re.search(r'\w*SERVER=\w*', connectStr).group(0)[7:]
                    user = re.search(r'\w*UID=\w*', connectStr).group(0)[4:]
                    password = re.search(r'\w*PWD=\w*', connectStr).group(0)[4:]
                    database = re.search(r'\w*DATABASE=\w*', connectStr).group(0)[9:]

                    render_er('mysql+pymysql://' + user + ':' + password + '@' + host + '/' + database + '',
                              '' + host + '->' + database + '.png')

                    response = base64.b64encode(open(host + '->' + database + '.png', "rb").read())

                    return JsonResponse({'status': 'ok', 'image': str(response)}, safe=True)
            Connect = pyodbc.connect(connectStr)
            taskid = 0
            for i in data:
                taskid = int(i)
                try:
                    ans = Answers.objects.get(TestPerson=personForTest,
                                              TestTask=TestTask.objects.get(Task=Task.objects.get(id=taskid),
                                                                            Test=test))
                    ans.Answer = data[i]
                    ans.save()
                except:
                    ans = Answers.objects.create(TestPerson=personForTest,
                                                 TestTask=TestTask.objects.get(Task=Task.objects.get(id=taskid),
                                                                               Test=test),
                                                 Answer=data[i])
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
                        fail = re.search(r'\'\w*[^\']*', result).group(0)
                        result = "<p>В вашем SQL запросе были найдены ошибки! </p><p>Проверьте правильность написания слов <div id=\"fail_text\">" + fail + '\'</div></p>'
                    # table.append(error)
                    return JsonResponse({'status': 'error', 'error': result}, charset="utf-8", safe=True)
            return JsonResponse({'status': 'ok', 'table': table, 'task': taskid}, charset="utf-8", safe=True)
        else:

            # Проверка ответов студента и их сохранение в базу, после нажатия на кнопку завершения
            test = Test.objects.get(id=int(testid))
            task = Task.objects.all()
            personForTest = TestPerson.objects.get(Person=request.user.id, Test=test, Variant=int(var))
            connectdb = TestConnectDataBase.objects.get(Test=test)
            connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase)
            Connect = pyodbc.connect(connectStr.ConnectionString)
            ConnectShadow = pyodbc.connect(connectStr.ShadowConnectionString)
            answ = 0
            weight = 0
            if test.HardCheck != True:
                for i in data:
                    temp = i.split(" ")[1]
                    try:
                        ans = Answers.objects.get(TestPerson=personForTest,
                                                TestTask=TestTask.objects.get(Task=Task.objects.get(id=temp), Test=test))
                        ans.Answer = data[i]
                        ans.save()
                    except Exception as e:
                        print(e)
                        ans = Answers.objects.create(TestPerson=personForTest,
                                                    TestTask=TestTask.objects.get(Task=Task.objects.get(id=temp),
                                                                                Test=test),
                                                    Answer=data[i])
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
                    except Exception as e:
                        print(e)
                        weight += task.get(id=temp).Weight

                personForTest.Mark = round(float(100 * answ / weight))
                personForTest.save()
                return JsonResponse({'status': 'ok'}, charset="utf-8", safe=True)
            else:
                for i in data:
                    temp = i.split(" ")[1]
                    try:
                        ans = Answers.objects.get(TestPerson=personForTest, TestTask=TestTask.objects.get(Task=Task.objects.get(id=temp), Test=test))
                        ans.Answer = data[i]
                        ans.save()
                    except Exception as e:
                        print(e)
                        ans = Answers.objects.create(TestPerson = personForTest, TestTask=TestTask.objects.get(Task=Task.objects.get(id=temp),Test=test),Answer=data[i])

                    try:
                        l=[]
                        l1=[]
                        sl=[]
                        sl1=[]
                        curs= Connect.cursor()
                        curs.execute(data[i])
                        l = [row for row in curs]
                        column_name = [row[0] for row in curs.description]
                        curs = Connect.cursor()
                        curs.execute(str(task.get(id=int(temp)).WTask))
                        l1=[row for row in curs]
                        column_name_w = [row[0] for row in curs.description]
                        Shadowcurs = ConnectShadow.cursor()
                        Shadowcurs.execute(data[i])
                        sl=[row for row in Shadowcurs]
                        column_name_shadow = [row[0] for row in Shadowcurs.description]
                        Shadowcurs = ConnectShadow.cursor()
                        Shadowcurs.execute(str(task.get(id=int(temp)).WTask))
                        sl1=[row for row in Shadowcurs]
                        column_name_w_shadow = [row[0] for row in Shadowcurs.description]

                        dic_check_student_light_table = {}
                        dic_check_student_shadow_table={}
                        dic_check_teacher_light_table={}
                        dic_check_teacher_shadow_table={}

                        for j in range(len(column_name)):
                            dic_check_student_light_table[column_name[j]] = [row[j] for row in l]

                        for j in range(len(column_name_shadow)):
                            dic_check_student_shadow_table[column_name_shadow[j]] = [row[j] for row in sl]

                        for j in range(len(column_name_w)):
                            dic_check_teacher_light_table[column_name_w[j]] = [row[j] for row in l1]

                        for j in range(len(column_name_shadow)):
                            dic_check_teacher_shadow_table[column_name_w_shadow[j]] = [row[j] for row in sl1]

                        if dic_check_student_light_table == dic_check_teacher_light_table and dic_check_student_shadow_table == dic_check_teacher_shadow_table:
                            answ += task.get(id=temp).Weight
                            weight += task.get(id=temp).Weight
                        else:
                            weight += task.get(id=temp).Weight
                    except Exception as e:
                        print(e)
                        weight += task.get(id=temp).Weight
                personForTest.Mark = round(float(100*answ/weight))
                personForTest.save()
                return JsonResponse({'status':'ok'}, charset="utf-8", safe=True)

    else:
        # Формирование страниц для теста
        # Определение теста, студента, который проходит тест
        tests = Test.objects.get(id=int(testid))
        task = Task.objects.all()
        connectdb = TestConnectDataBase.objects.get(Test=tests)
        connectStr = ConnectDataBase.objects.get(NameConnection=connectdb.ConnectDataBase)
        Connect = pyodbc.connect(connectStr.ConnectionString)
        personForTest = TestPerson.objects.get(Person=request.user.id, Test=tests, Variant=int(var))
        test = TestTask.objects.filter(Test=tests, Variant=int(var))
        CheckAnswer = False
        # Проверка наличия ответов на этот тест
        for q in test:
            if len(Answers.objects.filter(TestPerson=personForTest, TestTask=q)) == 0:
                CheckAnswer = False
            else:
                CheckAnswer = True
                continue
                # Запуск таймера
        tz = timezone('Asia/Omsk')
        if personForTest.Mark == None and tests.DateActivate <= datetime.now(tz):
            if (personForTest.StartTest == None):
                time = datetime.now(tz)
                personForTest.StartTest = time
                personForTest.save()
            else:
                time = personForTest.StartTest
            # Если ответов нет, то отдаётся страница с пустыми полями для заполнения


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
            if CheckAnswer == False:
                return render(request, "TestProject/test.html", {"GTest": test, "time": time, 'Monster': finalMonster})
            else:
                answers = {}
                for w in test:
                    answers[w.get_task().get_id()] = Answers.objects.get(TestPerson=personForTest,
                                                                         TestTask=w).get_answer()
                return render(request, "TestProject/test.html",
                              {"GTest": test,
                               "time": time,
                               'Monster': finalMonster,
                               "answers": answers})
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
                                right_check = Answers.objects.get(TestTask=i, TestPerson=tp).RightCheck
                                if right_check == 0 or right_check == False:
                                    tmp.append("Нет")
                                else:
                                    if right_check == 1 or right_check == True:
                                        tmp.append("Да")
                                    else:
                                        tmp.append(right_check)
                                #print(tmp)
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
                student = MyUser.objects.filter(GP=GP.objects.get(NameGP__contains=data['Group']))
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
                subtasks = Task.objects.filter(Category=Category.objects.get(id=i), Vision=True)
                if (subtasks.count() != 0):
                    for task in subtasks:
                        di = {}
                        table = []
                        try:
                            Connect = psycopg2.connect(task.get_connectdatabase().ConnectionString)
                        except:
                            Connect = pyodbc.connect(task.get_connectdatabase().ConnectionString)
                        #Connect = pyodbc.connect(task.get_connectdatabase().ConnectionString)
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
            if len(tasks) == 0:
                return JsonResponse({'status': 'error', 'error_message':'В выбранных категориях нет доступных заданий. Обратитесь к администратору системы.'}, charset="utf-8", safe=True)

            return JsonResponse({'status': 'ok', 'tasks': tasks}, charset="utf-8", safe=True)
        if data['check_task'] == "True":
            task = Task.objects.get(id=int(data['id']))
            Connect = 1
            try:
                Connect = psycopg2.connect(task.ConnectDataBase.ConnectionString)
            except:
                Connect = pyodbc.connect(task.ConnectDataBase.ConnectionString)
            curs = Connect.cursor()
            table = []
            l = []
            l2 = []
            isEquals = 'False'
            try:
                dic_1 = {}
                dic_2 = {}
                curs.execute(data['user_query'])
                l = [row for row in curs]
                col = [column[0] for column in curs.description]
                curs.execute(str(task.WTask))
                l2 = [row for row in curs]
                col2=[column[0] for column in curs.description]
                for j in range(len(col)):
                    dic_1[col[j]] = [row[j] for row in l]
                for j in range(len(col2)):
                    dic_2[col2[j]] = [row[j] for row in l2]
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
                    fail = re.search(r'\'\w*[^\']*', result).group(0)
                    result = "<p>В вашем SQL запросе были найдены ошибки! </p><p>Проверьте правильность написания слов <div id=\"fail_text\">" + fail + '\'</div></p>'
                # table.append(error)
                return JsonResponse({'status': 'error', 'error': result}, charset="utf-8", safe=True)
            if dic_1 == dic_2 and table[0] != "error":
                isEquals = 'True'
            return JsonResponse({'status': 'ok', 'table': table, 'task': task.id, 'isEquals': isEquals},
                                charset="utf-8", safe=True)
        if data['GetDBSchema'] != 'False':
            connection_string = Task.objects.get(
                id=int(data['GetDBSchema'])).get_connectdatabase().get_connection_string()
            try:
                host = re.search(r'\w*SERVER=\w*', connection_string).group(0)[7:]
                user = re.search(r'\w*UID=\w*', connection_string).group(0)[4:]
                password = re.search(r'\w*PWD=\w*', connection_string).group(0)[4:]
                database = re.search(r'\w*DATABASE=\w*', connection_string).group(0)[9:]

                render_er('mysql+pymysql://' + user + ':' + password + '@' + host + '/' + database + '',
                          '' + host + '->' + database + '.png')
            except:
                host = re.search(r'\w*host=\w*', connection_string).group(0)[5:]
                user = re.search(r'\w*user=\w*', connection_string).group(0)[5:]
                password = re.search(r'\w*password=\w*', connection_string).group(0)[9:]
                database = re.search(r'\w*dbname=\w*', connection_string).group(0)[7:]

                render_er('postgresql+psycopg2://' + user + ':' + password + '@' + host + '/' + database + '',
                          '' + host + '->' + database + '.png')

            response = base64.b64encode(open(host + '->' + database + '.png', "rb").read())

            return JsonResponse({'status': 'ok', 'image': str(response)}, safe=True)

    categories = Category.objects.all()
    return render(request, 'TestProject/trainer-2.html', {'categories': categories})


def ShowUsers(request):
    if request.user.is_superuser:
        if request.is_ajax():
            data = json.loads(request.read().decode("utf-8"))
            if data['resetPassword'] == "True":
                a = MyUser.objects.get(id=data['user_id'])
                a.set_password("Qwerty1234")
                a.save()
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
