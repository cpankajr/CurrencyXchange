from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication   # noqa F401

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils.encoding import smart_str
# from django.utils.safestring import mark_safe

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, \
    HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.views.decorators.clickjacking import xframe_options_exempt

import json
import datetime
import logging
import time
import uuid
import sys
import threading

from CurrencyExngApp.models import *
from CurrencyExngApp.utils import *

logger = logging.getLogger(__name__)


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return

def HomePage(request):
    if request.user.is_authenticated():
        return render(request, 'CurrencyExngApp/home.html')
    else:
        return HttpResponseRedirect("/login")

def LoginPage(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home")
    else:
        return render(request, 'CurrencyExngApp/login.html')

def SignupPage(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home")
    else:
        return render(request, 'CurrencyExngApp/signup.html')

def Profile(request):
    if request.user.is_authenticated():
        return render(request, 'CurrencyExngApp/profile.html')
    else:
        return HttpResponseRedirect("/login")

def Logout(request):  # noqa: N802
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect("/login")

class LoginSubmitAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data

            username = data['username']
            username = removeHtmlFromString(username)
            password = data['password']
            password = removeHtmlFromString(password)

            if len(User.objects.filter(username= username))==0:
                response['status'] = 301
            else:
                try:
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    response['status'] = 200
                except Exception as e:
                    response['status'] = 302
        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("LoginSubmitAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)

class SignUpAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data

            username = data['username']
            username = removeHtmlFromString(username)
            password = data['password']
            password = removeHtmlFromString(password)
            if len(User.objects.filter(username= username))>0:
                response['status'] = 301
            else:    
                User.objects.create(username= username, password=password)
                response['status'] = 200
        except Exception as e:  # noqa: F841
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("SignUpAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)

LoginSubmit = LoginSubmitAPI.as_view()
SignUp = SignUpAPI.as_view()


