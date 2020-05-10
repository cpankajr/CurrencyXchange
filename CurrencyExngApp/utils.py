from CurrencyExngApp.models import *
from django.conf import settings
import re
import json
import logging

logger = logging.getLogger(__name__)

def removeHtmlFromString(raw_str):
    regex_cleaner = re.compile('<.*?>')
    cleaned_raw_str = re.sub(regex_cleaner, '', raw_str)
    return cleaned_raw_str