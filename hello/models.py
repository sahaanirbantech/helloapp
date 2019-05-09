from django.db import models
from django.utils.dateparse import parse_date

# Create your models here.

class Hello(models.Model):
    username = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=10)

    def get_record(self):
        return self.username + ' has birthday on ' + self.date_of_birth
