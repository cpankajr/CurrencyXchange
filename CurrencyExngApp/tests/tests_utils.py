# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase

from CurrencyExngApp.utils import get_currency_symbol

import logging
logger = logging.getLogger(__name__)

"""
Tests for utils.py
"""


class UtilsFunctions(TestCase):

    def setUp(self):
        logger.info(
            "Setting up the test environment for utils.py...")

    """
    function tested: get_currency_symbol
    input:
        query containing currency code.
    expected output:
        returns respective currency symbol if present else None
    checks for:
        same expected output and output from function tested
    """

    def test_get_currency_symbol(self):
        logger.info("Testing get_currency_symbol...")
        currency_symbol = get_currency_symbol('usd')
        expected_currency_symbol = 'US$'
        self.assertEqual(currency_symbol,expected_currency_symbol)

        currency_symbol = get_currency_symbol('uvuyvysd')
        expected_currency_symbol = None
        self.assertEqual(currency_symbol,expected_currency_symbol)
