from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#User DB
class User(AbstractUser):
    GENDER_TYPES = (('m','male'), ('f','female'), ('o','other'))
    gender = models.CharField(max_length = 6, choices = GENDER_TYPES, default ='other')


#other DB