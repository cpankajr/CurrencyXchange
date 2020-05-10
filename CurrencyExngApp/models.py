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

    currency = models.CharField(max_length=500)

    ammount = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"


class Transaction(models.Model):

    sent_user = models.ForeignKey(User, null=True, blank=True,
                            on_delete=models.CASCADE, related_name="sending_user")

    sent_curr = models.CharField(max_length=500)

    sent_ammount = models.FloatField(default=0.0)

    recieved_user = models.ForeignKey(User, null=True, blank=True,
                            on_delete=models.CASCADE, related_name="receiving_user")

    recieved_curr = models.CharField(max_length=500)

    recieved_ammount = models.FloatField(default=0.0)

    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
