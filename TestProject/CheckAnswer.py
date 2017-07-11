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



def ExecuteAnswer(Connect, Answer,HardCheck):
    if HardCheck == 0:
        curs = Connect.cursor()                            
        curs.execute(Answer)
        l = [row for row in curs]
        curs.close()
        return l
    else:
        curs = Connect.cursor()
        curs.execute(Answer)
        l = [row for row in curs]
        column_name = [row[0] for row in curs.description]
        curs.close()
        return l,column_name


#personForTest - объект хранит подписку на тест конкретного пользователя на вариант теста (PersonTest)
#test - объект хранит данные о тесте (Test)
#var - вариант теста (int)
#UserAnswer -ответ пользователя (str)
#Connect - Объект, через который устанавливается соединение с открытой БД
#ConnectShadow - Объект, через который устанавливается соединение с теневой БД
#task - объект хранит данные о вопросе (Task)
#answ - баллы, полученные за правильные ответы
#weight - максимальное количество баллов за тест
def SaveAnswerWithOutHardCheck(personForTest,test,var, UserAnswer,Connect,ConnectShadow,task, answ, weight, HardCheck):
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
                #Ответ студента в открытую БД               
                OpenBDStudent = ExecuteAnswer(Connect, UserAnswer[i],HardCheck)
                                
                #Правильный запрос в открытую БД
                OpenBDTeacher = ExecuteAnswer(Connect,str(task.get(id=int(temp)).WTask),HardCheck)
                                
                #Ответ студента в теневую БД
                ShadowBDStudent = ExecuteAnswer(ConnectShadow,UserAnswer[i],HardCheck)
                                
                #Правильный запрос в теневую БД
                ShadowBDTeacher = ExecuteAnswer(ConnectShadow,str(task.get(id=int(temp)).WTask),HardCheck)
                                
                if OpenBDTeacher == OpenBDStudent and ShadowBDTeacher == ShadowBDStudent:
                                    
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
def CheckAnswerWithHardCheck(personForTest,test,var, UserAnswer,Connect,ConnectShadow,task, answ, weight, HardCheck):
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

                OpenBDStudent,ColumnNameOpBDSt = ExecuteAnswer(Connect,UserAnswer[i],HardCheck)

                
                OpenBDTeacher,ColumnNameOpBDTech = ExecuteAnswer(Connect,str(task.get(id=int(temp)).WTask),HardCheck)

                
                ShadowBDStudent,ColumnNameShBDSt= ExecuteAnswer(ConnectShadow,UserAnswer[i],HardCheck)

                
                ShadowBDTeacher,ColumnNameShBDTech = ExecuteAnswer(ConnectShadow,str(task.get(id=int(temp)).WTask),HardCheck)            

                dic_check_student_light_table = {}
                dic_check_student_shadow_table = {}
                dic_check_teacher_light_table = {}
                dic_check_teacher_shadow_table = {}

                for j in range(len(ColumnNameOpBDSt)):
                    dic_check_student_light_table[ColumnNameOpBDSt[j]] = [row[j] for row in OpenBDStudent]

                for j in range(len(ColumnNameShBDSt)):
                    dic_check_student_shadow_table[ColumnNameShBDSt[j]] = [row[j] for row in ShadowBDStudent]

                for j in range(len(ColumnNameOpBDTech)):
                    dic_check_teacher_light_table[ColumnNameOpBDTech[j]] = [row[j] for row in OpenBDTeacher]

                for j in range(len(ColumnNameShBDTech)):
                    dic_check_teacher_shadow_table[ColumnNameShBDTech[j]] = [row[j] for row in ShadowBDTeacher]

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