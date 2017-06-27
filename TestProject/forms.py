from django.forms.extras import SelectDateWidget
from django.utils.datetime_safe import datetime

from .models import *
from django import forms

BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')


class TestForm(forms.Form):
	Name = forms.CharField\
        (
            label='Название теста',
            max_length=30,
            required=True
        )
	Time = forms.IntegerField\
		(
			label="Время на прохождение",
			min_value=0,
			initial=0,
			help_text="(мин)",
			required=True
		)
	Variants = forms.IntegerField\
    	(
    		label = "Необходимое количество вариантов",
			min_value=0,
			initial=0,
			required=True
    	)
	ConnectDataBase = forms.ModelChoiceField\
		(
			label="База данных",
			queryset=ConnectDataBase.objects.all(),
			empty_label='Выбрать...',
			required=True
		)
		HardCheck = forms.BooleanField\
		(
			label = "Проверка по столбцам",
			required = False
		)

class TestPersonForm(forms.Form):
	Test = forms.ModelChoiceField\
		(
			label = "Выбор теста",
			queryset = Test.objects.all()
		)
	Person = forms.ModelMultipleChoiceField\
		(
			label = "Список студентов",
			queryset = MyUser.objects.all(),
			required=False
		)
	Group = forms.ModelMultipleChoiceField\
		(
			label = "Список групп",
			queryset = GP.objects.all(),
			required=False
		)

class AnswerForm(forms.Form):
	Test = forms.ModelChoiceField\
		(
			label = "Выбор теста",
			queryset = Test.objects.all()
		)
	Person = forms.ModelChoiceField\
		(
			label = "Список студентов",
			queryset = MyUser.objects.all(),
			required=False
		)
	Variant = forms.IntegerField\
    	(
    		label = "Вариант теста",
			min_value=0,
    	)