from CurrencyExngApp.models import *
from django.conf import settings
import re
import json
import logging
from forex_python.converter import CurrencyRates, CurrencyCodes
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64

logger = logging.getLogger(__name__)

"""
    function: removeHtmlFromString
    input:
        raw_str: raw stringwith html
    output:
        returns string after removing html tags
"""


def removeHtmlFromString(raw_str):
    regex_cleaner = re.compile('<.*?>')
    cleaned_raw_str = re.sub(regex_cleaner, '', raw_str)
    return cleaned_raw_str

"""
    function: currency_convert
    input:
        from_currency_code: currency currency code of amount currency
        to_currency_code: currency currency code of currency to which amount to be converted
        amount: amount for conversion
    output:
        returns converted ammount if succesfull else returns None
    """


def currency_convert(from_currency_code, to_currency_code, amount):
    try:
        currency_rate_obj = CurrencyRates()
        return currency_rate_obj.convert(from_currency_code.upper(), to_currency_code.upper(), float(amount))
    except Exception as e:
        return None

"""
    function: get_currency_symbol
    input:
        currency_code:  currency code
    output:
        returns respective currency symbol if present else None
"""


def get_currency_symbol(currency_code):
    currency_code_obj = CurrencyCodes()
    return currency_code_obj.get_symbol(currency_code.upper())

"""
    function: save_image
    input:
        image_data: binary data of image file
        image_data: image name (optional while uploading from console)
    output:
        returns file path on succesfull saving of image else returns None
"""


def save_image(image_data, image_name=None):
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
