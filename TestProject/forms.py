from .models import *
from django import forms
from django.forms.widgets import SelectDateWidget
from django.forms import ModelForm

class TestForm(forms.Form):
	Name = forms.CharField\
        (
            label=" Название теста",
            max_length=30,
            required=True
        )
	DateActivate = forms.DateTimeField\
		(
			label="Дата активации",
			input_formats=['%Y-%m-%d %H:%M'],
			required=True,
			help_text = 'YYYY-MM-DD HH:MM'
		)
	Variants = forms.IntegerField\
    	(
    		label = "Необходимое количество вариантов"	

    	)
	Time = forms.IntegerField\
    	(
    		label = "Время на прохождение"	

    	)
	TestPerson = forms.ModelChoiceField\
    	(

    		queryset = GP.objects.all(),
    		required = False

    	)
	ConnectDataBase = forms.ModelChoiceField\
    	(
			label = "Выберите БД",
			queryset = ConnectDataBase.objects.all(),
			required = False

    	)