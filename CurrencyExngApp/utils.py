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

def currency_convert(from_currency,to_currency,ammount):
	currency_rate_obj = CurrencyRates()
	return currency_rate_obj.convert(from_currency.upper(), to_currency.upper(), float(ammount))

def get_currency_symbol(currency_code):
	currency_rate_obj = CurrencyRates()
	return currency_rate_obj.get_symbol(currency_code)

