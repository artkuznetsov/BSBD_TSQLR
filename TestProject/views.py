#from django.http import HttpResponse
#from django.shortcuts import render_to_response
from .forms import *
from .models import models
from django.http import *
from django.shortcuts import *
from django.contrib.auth.models import User, UserManager

from django.contrib.auth.decorators import login_required



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


def PrimerTests(HttpRequest):
	try:
		tests = Test.objects.values("Name", "DateActivate", "Time")
	except:
		return HttpResponseServerError("Server error")
	return render(HttpRequest, "TestProject/tests.html",{"tests": tests})

@login_required(login_url='/accounts/login/')
def TestsUser(request):
	user = User.objects.get(id = request.user.id)
	UserTest = TestPerson.objects.filter(Person = user)
	mass = []
	for i in UserTest:
		mass.append(Test.objects.get(id = i.Test_id))
	
	return render(request,"TestProject/profile.html",
                  {
                      "TestUser": mass
                  })

def AddUsers(request):
	if (request.method == "POST"):
		Group = request.POST['Group']
		users = request.POST['users']
		users = users.split('\n')
		count = 0
		for i in users:

			user = i.split(' ')
			
			person =User.objects.create_user(
				username = Group + str(count),
				email =None,
				password = 'Qwerty123'+ str(count),
				last_name = user[0],
				first_name = user[1]
			)
			count+=1
			person.save()
		return HttpResponseRedirect("/TestProject/")
	else:
		return render(request, "TestProject/tests.html")


