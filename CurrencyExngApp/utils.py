from CurrencyExngApp.models import *
from django.conf import settings
import re
import json
import logging
from forex_python.converter import CurrencyRates

logger = logging.getLogger(__name__)

def removeHtmlFromString(raw_str):
    regex_cleaner = re.compile('<.*?>')
    cleaned_raw_str = re.sub(regex_cleaner, '', raw_str)
    return cleaned_raw_str

def currency_convert(from_currency_code,to_currency_code,amount):
	currency_rate_obj = CurrencyRates()
	return currency_rate_obj.convert(from_currency_code.upper(), to_currency_code.upper(), float(amount))

def get_currency_symbol(currency_code):
	currency_rate_obj = CurrencyRates()
	return currency_rate_obj.get_symbol(currency_code)

