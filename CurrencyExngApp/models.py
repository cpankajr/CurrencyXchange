from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.conf import settings
from slugify import slugify

import sys
import json
import logging

from CurrencyExngApp.utils import *


class User(AbstractUser):

    profile_image = models.ImageField(
        upload_to=settings.IMAGE_UPLOAD_PATH, null=True, blank=True, help_text="Profile Image")

    def name(self):
        return self.first_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.set_password(self.password)
        elif not self.password.startswith("pbkdf2_sha256$36000$"):
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Wallet(models.Model):

    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE)

    currency_code = models.CharField(max_length=500)

    amount = models.FloatField(default=0.0)

    def get_amount_string(self):
        currency_symbol = get_currency_symbol(self.currency_code)
        if currency_symbol is None:
            return str(self.amount)
        else:
            return str(currency_symbol) + " " + str(self.amount)

    def get_currency_symbol(self):
        currency_symbol = get_currency_symbol(self.currency_code)
        if currency_symbol is None:
            return "$"
        else:
            return currency_symbol

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __str__(self):
        return self.user.username+"'s Wallet"


class Transaction(models.Model):

    sent_user = models.ForeignKey(User, null=True, blank=True,
                            on_delete=models.CASCADE, related_name="sending_user")

    sent_curr_code = models.CharField(max_length=500)

    sent_amount = models.FloatField(default=0.0)

    recieved_user = models.ForeignKey(User, null=True, blank=True,
                            on_delete=models.CASCADE, related_name="receiving_user")

    recieved_curr_code = models.CharField(max_length=500)

    recieved_amount = models.FloatField(default=0.0)

    date = models.DateTimeField(default=timezone.now)

    reciept_pdf = models.FileField(
        upload_to="files", null=True, blank=True, help_text="Reciept PDF")

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def get_datetime(self):
        try:
            import pytz
            est = pytz.timezone(settings.TIME_ZONE)
            return self.date.astimezone(est).strftime("%b %d %Y %I:%M %p")
        except Exception:
            return self.date.strftime("%b %d %Y %I:%M %p")

    def get_recieved_amount_string(self):
        currency_symbol = get_currency_symbol(self.recieved_curr_code)
        if currency_symbol is None:
            return str(self.recieved_amount)
        else:
            return str(currency_symbol) + " " + str(self.recieved_amount)

    def get_sent_amount_string(self):
        currency_symbol = get_currency_symbol(self.sent_curr_code)
        if currency_symbol is None:
            return str(self.sent_amount)
        else:
            return str(currency_symbol) + " " + str(self.sent_amount)
