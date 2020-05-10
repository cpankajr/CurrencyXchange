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