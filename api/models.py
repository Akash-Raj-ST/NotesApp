from django.db import models
from django.core.exceptions import ValidationError

import string
import random


def gen_code():
    while True:
        a=''.join(random.choices(string.ascii_uppercase,k=4))
        b=''.join(random.choices(string.digits,k=4))
        code_seq = a+b

        if user.objects.filter(code = code_seq).count() == 0:
            break

    return code_seq

def min_length_8(value):
    if len(value)<8:
        raise ValidationError("Minimum length is 8")
    else:
        return value

def min_length_5(value):
    if len(value)<5:
        raise ValidationError("Minimum length is 5")
    else:
        return value

# Create your models here.
class user(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    name = models.CharField(validators=[min_length_5],max_length=20)
    user_name = models.CharField(unique=True,validators=[min_length_8],max_length=20)
    password = models.CharField(validators=[min_length_8],max_length=50)
    email = models.EmailField(unique=True, max_length=254)
    code = models.CharField(unique=True,default=gen_code,max_length=10)
    date_joined = models.DateField(auto_now_add=True)

class section(models.Model):
    section_id = models.BigAutoField(primary_key=True)
    section_name = models.CharField(max_length=25)
    user_id = models.ForeignKey('user', on_delete=models.CASCADE)

class box(models.Model):
    sect_box_id = models.BigAutoField(primary_key=True)
    box_name = models.CharField(max_length=25)
    section_id = models.ForeignKey("section", on_delete=models.CASCADE)

class files(models.Model):
    file_id = models.BigAutoField(primary_key=True)
    file_name = models.CharField( max_length=250)
    file_url = models.FileField(upload_to='files',null=True)
    sect_box_id = models.ForeignKey("box", on_delete=models.CASCADE)
