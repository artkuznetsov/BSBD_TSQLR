from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

from django.conf import settings
from TestProject.models import TestPerson, New

from django.http import *
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from datetime import *
from pytz import timezone
from django.db.models import Q
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
UserModel = get_user_model()


class MainPage(LoginRequiredMixin, TemplateView):
    template_name = "TestProject/base-2.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    def ajax(self, request, *args, **kwargs):
        data = json.loads(request.read().decode("utf-8"))
        user = request.user
        user.set_password(data['Password'])
        user.save()
        return JsonResponse({'status': 'ok'}, charset="utf-8", safe=True)

    def default_get(self, request, *args, **kwargs):
        subscribe = TestPerson.objects.filter(Person=request.user).order_by('Test__DateActivate')
        user = request.user
        with_mark = []
        without_mark = []
        tz = timezone('Asia/Omsk')
        for sub in subscribe:
            if sub.get_mark():
                with_mark.append(sub)
            else:
                if sub.Test.DateActivate <= datetime.now(tz):
                    without_mark.append(sub)

        context = {
                "completed_tests": with_mark,
                "uncompleted_tests": without_mark,
                "news": New.objects.filter(Q(Group=user.GP) | Q(Group__isnull=True))
        }

        return self.render_to_response(context)


    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.ajax(request)
        else:
            return self.default_get(request)