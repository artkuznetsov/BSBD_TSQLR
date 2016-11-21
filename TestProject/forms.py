from django.forms.extras import SelectDateWidget
from django.utils.datetime_safe import datetime

from .models import *
from django import forms
#from django.forms.widgets import DateTimeBaseInput
from django.forms import ModelForm, SplitDateTimeWidget
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget


class TestForm(forms.Form):
	Name = forms.CharField\
        (
            label=" Название теста",
            max_length=30,
            required=True,
			initial = "Тест"
        )
	DateActivate = forms.DateTimeField\
		(
			label="Дата активации",
			input_formats=['%Y-%m-%d %H:%M'],
			required=True,
			help_text = 'YYYY-MM-DD HH:MM',
			initial = datetime.now,
			widget = SplitDateTimeWidget
		)
	Time = forms.IntegerField\
		(
			label="Время на прохождение",
			min_value=0,
			initial=0
		)
	Variants = forms.IntegerField\
    	(
    		label = "Необходимое количество вариантов",
			min_value=0,
			initial=0
    	)