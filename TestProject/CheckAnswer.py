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
from .CreateShema import CreateShema
from .CheckAnswer import *

#personForTest - объект хранит подписку на тест конкретного пользователя на вариант теста (PersonTest)
#test - объект хранит данные о тесте (Test)
#var - вариант теста (int)
#UserAnswer -ответ пользователя (str)
#Connect - Объект, через который устанавливается соединение с открытой БД
#ConnectShadow - Объект, через который устанавливается соединение с теневой БД
#task - объект хранит данные о вопросе (Task)
#answ - баллы, полученные за правильные ответы
#weight - максимальное количество баллов за тест
def SaveAnswerWithOutHardCheck(personForTest,test,var, UserAnswer,Connect,ConnectShadow,task, answ, weight):
    for i in UserAnswer:
        temp = i.split(" ")[1]
        if temp == "Test":
            continue
        else:
            try:
                ans = Answers.objects.get(TestPerson=personForTest,
                                         TestTask=TestTask.objects.get(Task=Task.objects.get(id=temp), Test=test,Variant=var))
                ans.Answer = UserAnswer[i]
                ans.RightCheck = False
                ans.save()
            except Exception as e:
                print(e)
                ans = Answers.objects.create(TestPerson=personForTest,
                                            TestTask=TestTask.objects.get(Task=Task.objects.get(id=temp),
                                                                                       Test=test, Variant=var),
                                                         Answer=UserAnswer[i], RightCheck = False)
            try:
                               
                curs = Connect.cursor()
                                
                curs.execute(UserAnswer[i])
                l = [row for row in curs]
                                
                curs = Connect.cursor()
                curs.execute(str(task.get(id=int(temp)).WTask))
                l1 = [row for row in curs]
                                
                Shadowcurs = ConnectShadow.cursor()
                Shadowcurs.execute(UserAnswer[i])
                sl = [row for row in Shadowcurs]
                                
                Shadowcurs = ConnectShadow.cursor()
                Shadowcurs.execute(str(task.get(id=int(temp)).WTask))
                sl1 = [row for row in Shadowcurs]
                                
                if l1 == l and sl1 == sl:
                                    
                    answ += task.get(id=temp).Weight
                                    
                    answer_right = Answers.objects.get(TestPerson=personForTest, TestTask=TestTask.objects.get(Task=Task.objects.get(id=temp), Test=test, Variant=var), Answer=UserAnswer[i])
                                    
                    answer_right.RightCheck = True
                                    
                    answer_right.save()
                    weight += task.get(id=temp).Weight
                                    
                else:
                                    
                    weight += task.get(id=temp).Weight
                                    
            except Exception as e:
                               
                weight += task.get(id=temp).Weight
                with_exception = True
        return round(float(100 * answ / weight))


#personForTest - объект хранит подписку на тест конкретного пользователя на вариант теста (PersonTest)
#test - объект хранит данные о тесте (Test)
#var - вариант теста (int)
#UserAnswer -ответ пользователя (str)
#Connect - Объект, через который устанавливается соединение с открытой БД
#ConnectShadow - Объект, через который устанавливается соединение с теневой БД
#task - объект хранит данные о вопросе (Task)
#answ - баллы, полученные за правильные ответы
#weight - максимальное количество баллов за тест
def CheckAnswerWithHardCheck(personForTest,test,var, UserAnswer,Connect,ConnectShadow,task, answ, weight):
    for i in UserAnswer:
        temp = i.split(" ")[1]
        if temp == "Test":
            continue
        else:
            try:
                ans = Answers.objects.get(TestPerson = personForTest, TestTask = TestTask.objects.get(Task = Task.objects.get(id=temp), Test = test, Variant = var))
                            
                ans.Answer = UserAnswer[i]
                ans.RightCheck = False
                            
                ans.save()
                            
            except Exception as e:
                            
                ans = Answers.objects.create(TestPerson = personForTest, TestTask = TestTask.objects.get(Task=Task.objects.get(id=temp),Test=test, Variant=var), Answer=UserAnswer[i], RightCheck = False)
            try:
                l=[]
                l1=[]
                sl=[]
                sl1=[]

                curs = Connect.cursor()
                curs.execute(UserAnswer[i])
                l = [row for row in curs]
                column_name = [row[0] for row in curs.description]
                           
                curs1 = Connect.cursor()
                            
                curs1.execute(str(task.get(id=int(temp)).WTask))
                            
                l1 = [row for row in curs1]
                column_name_w = [row[0] for row in curs1.description]
                            
                Shadowcurs = Connect.cursor()
                Shadowcurs.execute(UserAnswer[i])
                sl = [row for row in Shadowcurs]
                column_name_shadow = [row[0] for row in Shadowcurs.description]
                            
                Shadowcurs1 = Connect.cursor()
                Shadowcurs1.execute(str(task.get(id=int(temp)).WTask))
                sl1 = [row for row in Shadowcurs1]
                column_name_w_shadow = [row[0] for row in Shadowcurs1.description]
                            

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
                    right_check = Answers.objects.get(TestPerson=personForTest, TestTask = TestTask.objects.get(Task=Task.objects.get(id=temp), Test=test, Variant=var), Answer=UserAnswer[i])
                    right_check.RightCheck = True
                    right_check.save()

                    weight += task.get(id=temp).Weight
                else:
                    weight += task.get(id=temp).Weight
            except Exception as e:
                            
                weight += task.get(id=temp).Weight
    return round(float(100 * answ / weight))