from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication   # noqa F401

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, \
    HttpResponseRedirect
from django.db.models import Q


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

SUPPORTED_CURRENCIES = {'EUR': 'EUR (€) (European Euro)',
                        'IDR': 'IDR (Rp) (Indonesian rupiah)',
                        'BGN': 'BGN (BGN) (Bulgarian lev)',
                        'ILS': 'ILS (₪) (Israeli new sheqel)',
                        'GBP': 'GBP (£) (British pound)',
                        'DKK': 'DKK (Kr) (Danish krone)',
                        'CAD': 'CAD ($) (Canadian dollar)',
                        'JPY': 'JPY (¥) (Japanese yen)',
                        'HUF': 'HUF (Ft) (Hungarian forint)',
                        'RON': 'RON (L) (Romanian leu)',
                        'MYR': 'MYR (RM) (Malaysian ringgit)',
                        'SEK': 'SEK (kr) (Swedish krona)',
                        'SGD': 'SGD (S$) (Singapore dollar)',
                        'HKD': 'HKD (HK$) (Hong Kong dollar)',
                        'AUD': 'AUD ($) (Australian dollar)',
                        'CHF': 'CHF (Fr.) (Swiss franc)',
                        'TRY': 'TRY (TRY) (Turkish new lira)',
                        'HRK': 'HRK (kn) (Croatian kuna)',
                        'NZD': 'NZD (NZ$) (New Zealand dollar)',
                        'THB': 'THB (฿) (Thai baht)',
                        'USD': 'USD (US$) (United States dollar)',
                        'NOK': 'NOK (kr) (Norwegian krone)',
                        'RUB': 'RUB (R) (Russian ruble)',
                        'INR': 'INR (₹) (Indian rupee)',
                        'MXN': 'MXN ($) (Mexican peso)',
                        'CZK': 'CZK (Kč) (Czech koruna)',
                        'BRL': 'BRL (R$) (Brazilian real)',
                        'PLN': 'PLN (zł) (Polish zloty)',
                        'PHP': 'PHP (₱) (Philippine peso)',
                        'ZAR': 'ZAR (R) (South African rand)'}


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


def RedirecttoHome(request):
    return HttpResponseRedirect("/home")


def HomePage(request):
    if request.user.is_authenticated():
        wallet_objs = Wallet.objects.filter(user=request.user)
        if len(wallet_objs) > 0:
            wallet_obj = wallet_objs[0]
        else:
            wallet_obj = None
        transaction_objs = Transaction.objects.filter(
            Q(sent_user=request.user) | Q(recieved_user=request.user))
        # print(transaction_objs)
        return render(request, 'CurrencyExngApp/home.html', {
            "wallet_obj": wallet_obj,
            "transaction_objs": transaction_objs.order_by("-pk"),
            "SUPPORTED_CURRENCIES": SUPPORTED_CURRENCIES
        })
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
        response['message'] = "Error"

        try:

            data = request.data

            username = data['username']
            username = removeHtmlFromString(username)
            password = data['password']
            password = removeHtmlFromString(password)

            if len(User.objects.filter(username=username)) == 0:
                response['status'] = 301
                response['message'] = "No user found"
            else:
                try:
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    response['status'] = 200
                    response['message'] = "Success"
                except Exception as e:
                    response['status'] = 302
                    response['message'] = "Wrong password"
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
        response['message'] = "Error"
        try:

            data = request.data

            username = data['username']
            username = removeHtmlFromString(username)
            password = data['password']
            password = removeHtmlFromString(password)
            if len(User.objects.filter(username=username)) > 0:
                response['status'] = 301
                response['message'] = "Username already exist"
            else:
                User.objects.create(username=username, password=password)
                response['status'] = 200
                response['message'] = "Success"
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
        response['message'] = "Error"
        try:

            data = request.data

            username = data['username']
            username = removeHtmlFromString(username)

            currency_code = data['currency_code']
            currency_code = removeHtmlFromString(currency_code)
            user = User.objects.get(username=username)
            if len(Wallet.objects.filter(user=user)) > 0:
                response['status'] = 301
                response['message'] = "Wallet already created."
            else:
                Wallet.objects.create(user=user, currency_code=currency_code)
                response['status'] = 200
                response['message'] = "Success"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("CreateWalletAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)


class ReadWalletAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        response['message'] = "Error"
        try:

            data = request.data

            username = data['username']
            username = removeHtmlFromString(username)

            if len(User.objects.filter(username=username)) > 0:
                user_obj = User.objects.filter(username=username)[0]
                wallet_obj = Wallet.objects.get(user=user_obj)

                response['wallet_balance'] = wallet_obj.get_amount_string()
                response['status'] = 200
                response['message'] = "Success"
            else:
                response['status'] = 301
                response['message'] = "Username not exist"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("ReadWalletAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)


class ConvertCurrencyAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        response['message'] = "Error"
        try:

            data = request.data

            from_currency_code = data['from_currency_code']
            from_currency_code = removeHtmlFromString(from_currency_code)

            to_currency_code = data['to_currency_code']
            to_currency_code = removeHtmlFromString(to_currency_code)

            amount = data['amount']
            amount = removeHtmlFromString(amount)
            converted_amount = currency_convert(
                from_currency_code, to_currency_code, amount)
            if converted_amount is not None:
                response['converted_amount'] = converted_amount
            response['status'] = 200
            response['message'] = "Success"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("ConvertCurrencyAPI: %s at %s",
                         e, str(exc_tb.tb_lineno))

        return Response(data=response)


class SendMoneyAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        response['message'] = "Error"
        try:

            data = request.data

            from_username = data['from_username']
            from_username = removeHtmlFromString(from_username)

            to_username = data['to_username']
            to_username = removeHtmlFromString(to_username)

            amount = data['amount']
            amount = removeHtmlFromString(amount)
            if len(User.objects.filter(username=to_username)) > 0:

                sending_user = User.objects.get(username=from_username)
                recieving_user = User.objects.get(username=to_username)

                sending_wallet_obj = Wallet.objects.get(user=sending_user)
                if float(amount) > sending_wallet_obj.amount:
                    response['status'] = 302
                    response['message'] = "Sent amount greater than wallet amount"
                else:
                    try:
                        recieving_wallet_obj = Wallet.objects.get(
                            user=recieving_user)
                    except Exception as e:
                        recieving_wallet_obj = None
                    if recieving_wallet_obj is not None:
                        from_currency_code = sending_wallet_obj.currency_code
                        to_currency_code = recieving_wallet_obj.currency_code

                        converted_amount = currency_convert(
                            from_currency_code, to_currency_code, amount)

                        sending_wallet_obj.amount = sending_wallet_obj.amount - \
                            float(amount)
                        recieving_wallet_obj.amount = recieving_wallet_obj.amount + \
                            float(converted_amount)

                        sending_wallet_obj.save()
                        recieving_wallet_obj.save()
                        Transaction.objects.create(sent_user=sending_user, sent_curr_code=from_currency_code, sent_amount=amount,
                                                   recieved_user=recieving_user, recieved_curr_code=to_currency_code, recieved_amount=converted_amount)
                        response['status'] = 200
                        response['message'] = "Success"
                    else:
                        response['status'] = 303
                        response['message'] = "Recieving user not found"

            else:
                response['status'] = 301
                response['message'] = "Username not found"
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
        response['message'] = "Error"
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
            Transaction.objects.create(
                sent_user=user, sent_curr_code=wallet_obj.currency_code, sent_amount=amount)
            response['status'] = 200
            response['message'] = "Success"
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
        response['message'] = "Error"
        try:

            data = request.data

            username = data['username']
            username = removeHtmlFromString(username)

            first_name = data['first_name']
            first_name = removeHtmlFromString(first_name)

            last_name = data['last_name']
            last_name = removeHtmlFromString(last_name)

            emailid = data['emailid']
            emailid = removeHtmlFromString(emailid)

            image_data = data['image_data']

            user_obj = User.objects.get(username=username)
            if image_data != "":
                if "image_name" in data:
                    file_path = save_image(image_data, data["image_name"])
                else:
                    file_path = save_image(image_data)

                if file_path is None:
                    response['status'] = 301
                else:
                    user_obj.profile_image = file_path

            user_obj.first_name = first_name
            user_obj.last_name = last_name
            user_obj.email = emailid
            user_obj.save()

            response['status'] = 200
            response['message'] = "Success"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("SaveProfileAPI: %s at %s", e, str(exc_tb.tb_lineno))

        return Response(data=response)


class GetAnalyticsAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        response['message'] = "Error"
        try:

            data = request.data

            start_datetime = data['start_date']
            start_datetime = datetime.datetime.strptime(
                start_datetime, '%d-%m-%Y')

            end_datetime = data['end_date']
            end_datetime = datetime.datetime.strptime(end_datetime, '%d-%m-%Y')

            username = data['username']

            user_obj = User.objects.get(username=username)
            transaction_objs = Transaction.objects.filter(
                date__date__gte=start_datetime, date__date__lte=end_datetime, sent_user=user_obj).filter(~Q(recieved_user=None))

            overrall_transaction = 0
            all_details = []
            for transaction_obj in transaction_objs:
                from_currency_code = transaction_obj.sent_curr_code
                to_currency_code = transaction_obj.recieved_curr_code
                amount = transaction_obj.sent_amount
                sent_amount = transaction_obj.recieved_amount
                converted_amount = currency_convert(
                    from_currency_code, to_currency_code, amount)

                transaction_in_user_currency = currency_convert(
                    to_currency_code, from_currency_code, sent_amount - converted_amount)
                overrall_transaction += transaction_in_user_currency
                all_details.append({
                    "from_currency_code": from_currency_code,
                    "to_currency_code": to_currency_code,
                    "datetime": transaction_obj.date.strftime("%d-%m-%Y, %H:%M:%S"),
                    "amount_sent": amount,
                    "amount_after_coversion_while_transaction": sent_amount,
                    "amount_after_coversion_now": converted_amount,
                    "profitable_transaction": transaction_in_user_currency > 0,
                })
            if overrall_transaction < 0:
                response["type"] = "loss"
                response["amount"] = overrall_transaction
                response["all_details"] = all_details
            elif overrall_transaction > 0:
                response["type"] = "profit"
                response["amount"] = overrall_transaction
                response["all_details"] = all_details
            else:
                response["type"] = "breakeven"
                response["amount"] = overrall_transaction
                response["all_details"] = all_details
            response['status'] = 200
            response['message'] = "Success"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("GetAnalyticsAPI: %s at %s",
                         e, str(exc_tb.tb_lineno))

        return Response(data=response)


class GetOverallAnalyticsAPI(APIView):

    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, *args, **kwargs):

        response = {}
        response['status'] = 500
        response['message'] = "Error"
        try:

            data = request.data

            username = data['username']

            user_obj = User.objects.get(username=username)

            if user_obj.is_staff:
                start_datetime = data['start_date']
                start_datetime = datetime.datetime.strptime(
                    start_datetime, '%d-%m-%Y')

                end_datetime = data['end_date']
                end_datetime = datetime.datetime.strptime(
                    end_datetime, '%d-%m-%Y')

                transaction_objs = Transaction.objects.filter(
                    date__date__gte=start_datetime, date__date__lte=end_datetime)
                analytics = {}
                days = ["Monday", "Tuesday", "Wednesday",
                        "Thursday", "Friday", "Saturday", "Sunday"]
                all_details = []
                for i in range(7):
                    txn_objs = transaction_objs.filter(date__date__week_day=i)
                    analytics[days[i]] = 0
                    for transaction_obj in txn_objs:
                        from_currency_code = transaction_obj.sent_curr_code
                        sent_amount = transaction_obj.sent_amount
                        transaction_amnt_in_usd = currency_convert(
                            from_currency_code, 'usd', sent_amount)
                        converted_amount = transaction_amnt_in_usd
                        analytics[days[i]] += converted_amount
                        all_details.append({
                            "amount_sent": transaction_amnt_in_usd,
                            "datetime": transaction_obj.date.strftime("%d-%m-%Y, %H:%M:%S"),
                        })

                response['analytics'] = analytics
                response['all_details'] = all_details
                response['status'] = 200
                response['message'] = "Success"
            else:
                response['status'] = 403
                response['message'] = "You are not autherized to this api"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("GetOverallAnalyticsAPI: %s at %s",
                         e, str(exc_tb.tb_lineno))

        return Response(data=response)


LoginSubmit = LoginSubmitAPI.as_view()
GetAnalytics = GetAnalyticsAPI.as_view()
GetOverallAnalytics = GetOverallAnalyticsAPI.as_view()
SignUp = SignUpAPI.as_view()
AddMoney = AddMoneyAPI.as_view()
SendMoney = SendMoneyAPI.as_view()
CreateWallet = CreateWalletAPI.as_view()
ConvertCurrency = ConvertCurrencyAPI.as_view()
SaveProfile = SaveProfileAPI.as_view()
ReadWallet = ReadWalletAPI.as_view()
