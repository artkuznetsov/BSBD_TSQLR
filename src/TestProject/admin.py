from django.contrib import admin
from .models import *
from django import forms
# from django.forms.widgets import SelectDateWidget
from django.contrib.auth.models import User
from .forms import *
	


admin.site.register(ConnectDataBase)
admin.site.register(Task)
admin.site.register(Category)
admin.site.register(New)
admin.site.register(Test)
admin.site.register(TestPerson)
admin.site.register(DataBaseType)
admin.site.register(MyUser)
