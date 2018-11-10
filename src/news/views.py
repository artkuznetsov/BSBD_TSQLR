from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

from django.conf import settings
from TestProject.models import New

from django.http import *
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from datetime import *
from pytz import timezone
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
UserModel = get_user_model()


class NewDetailView(LoginRequiredMixin, DetailView):

    template_name = "TestProject/new.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    slug_field = 'id'

    def get_queryset(self):
        return New.objects.filter(Q(Group=self.request.user.GP) | Q(Group__isnull=True))