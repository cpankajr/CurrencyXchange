from CurrencyExngApp.models import *
from django.conf import settings
import re
import json
import logging
from forex_python.converter import CurrencyRates,CurrencyCodes
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64

logger = logging.getLogger(__name__)

def removeHtmlFromString(raw_str):
    regex_cleaner = re.compile('<.*?>')
    cleaned_raw_str = re.sub(regex_cleaner, '', raw_str)
    return cleaned_raw_str

def currency_convert(from_currency_code,to_currency_code,amount):
    try:
        currency_rate_obj = CurrencyRates()
        return currency_rate_obj.convert(from_currency_code.upper(), to_currency_code.upper(), float(amount))
    except Exception as e:
        return None

def get_currency_symbol(currency_code):
    currency_code_obj = CurrencyCodes()
    return currency_code_obj.get_symbol(currency_code.upper())

def save_image(image_data,image_name=None):
    try:
        file_extention = image_data.name.split(".")[-1]
        file_extention = file_extention.lower()
        if file_extention in ["png", "jpg", "jpeg", "svg", "bmp", "gif", "tiff", "exif", "jfif"]:
            path = default_storage.save(
                image_data.name.replace(" ", ""), ContentFile(image_data.read()))
            return path
        else:
            return None
    except Exception as e:
        if image_name:
            file_extention = image_name.split(".")[-1]
            file_extention = file_extention.lower()
            if file_extention in ["png", "jpg", "jpeg", "svg", "bmp", "gif", "tiff", "exif", "jfif"]:
                path = default_storage.save(
                    image_name.replace(" ", ""), ContentFile(base64.b64decode(image_data)))
                return path
            else:
                return None
        return None