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
        except Exception as e:
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
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("SignUpAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)

class CreateWalletAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data

            username = data['username']
            username = removeHtmlFromString(username)

            currency_code = data['currency_code']
            currency_code = removeHtmlFromString(currency_code)
            user = User.objects.get(username=username)
            if len(Wallet.objects.filter(user= user))>0:
                response['status'] = 301
            else:
                Wallet.objects.create(user= user, currency_code=currency_code)
                response['status'] = 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("CreateWalletAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)

class ConvertCurrencyAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data

            from_currency_code = data['from_currency_code']
            from_currency_code = removeHtmlFromString(from_currency_code)

            to_currency_code = data['to_currency_code']
            to_currency_code = removeHtmlFromString(to_currency_code)

            amount = data['amount']
            amount = removeHtmlFromString(amount)
            converted_amount = currency_convert(from_currency_code,to_currency_code,amount)
            if converted_amount is not None:
                response['converted_amount'] =  converted_amount  
            response['status'] = 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("ConvertCurrencyAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)

class SendMoneyAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data

            from_username = data['from_username']
            from_username = removeHtmlFromString(from_username)

            to_username = data['to_username']
            to_username = removeHtmlFromString(to_username)

            amount = data['amount']
            amount = removeHtmlFromString(amount)
            if len(User.objects.filter(username= to_username))>0:

                sending_user = User.objects.get(username=from_username)
                recieving_user = User.objects.get(username=to_username)
                
                sending_wallet_obj = Wallet.objects.get(user=sending_user)
                if float(amount)>sending_wallet_obj.amount:
                    response['status'] = 302
                else:
                    try:
                        recieving_wallet_obj = Wallet.objects.get(user=recieving_user)
                    except Exception as e:
                        recieving_wallet_obj = None
                    if recieving_wallet_obj is not None:
                        from_currency_code = sending_wallet_obj.currency_code
                        to_currency_code = recieving_wallet_obj.currency_code

                        converted_amount = currency_convert(from_currency_code,to_currency_code,amount)

                        sending_wallet_obj.amount = sending_wallet_obj.amount - float(amount)
                        recieving_wallet_obj.amount = recieving_wallet_obj.amount + float(converted_amount)

                        sending_wallet_obj.save()
                        recieving_wallet_obj.save()
                        Transaction.objects.create(sent_user=sending_user ,sent_curr_code=from_currency_code,sent_amount=amount,
                            recieved_user=recieving_user,recieved_curr_code=to_currency_code,recieved_amount=converted_amount)
                        response['status'] = 200
                    else:
                        response['status'] = 303        
                            
            else:    
                response['status'] = 301
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("SendMoneyAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)

class AddMoneyAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data

            username = data['username']
            username = removeHtmlFromString(username)

            amount = data['amount']
            amount = removeHtmlFromString(amount)
            
            user = User.objects.get(username=username)

            wallet_obj = Wallet.objects.get(user=user)
            wallet_obj.amount = wallet_obj.amount + float(amount)
            wallet_obj.save()
            Transaction.objects.create(sent_user=user ,sent_curr_code=wallet_obj.currency_code,sent_amount=amount)
            response['status'] = 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("AddMoneyAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)


class SaveProfileAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        try:

            data = request.data

            username = data['username']
            username = removeHtmlFromString(username)

            first_name = data['first_name']
            first_name = removeHtmlFromString(first_name)

            last_name = data['last_name']
            last_name = removeHtmlFromString(last_name)

            image_data = data['image_data']
            image_data = removeHtmlFromString(image_data)

            file_path = save_image(image_data)
            if file_path is None:
                response['status'] = 301
            else:
                response['file_path'] = file_path
                response['status'] = 200
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("SaveProfileAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)

LoginSubmit = LoginSubmitAPI.as_view()
SignUp = SignUpAPI.as_view()
AddMoney = AddMoneyAPI.as_view()
SendMoney = SendMoneyAPI.as_view()
CreateWallet = CreateWalletAPI.as_view()
ConvertCurrency = ConvertCurrencyAPI.as_view()
SaveProfile = SaveProfileAPI.as_view()