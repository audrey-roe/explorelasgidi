import random
from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class user_info_extend(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number= models.BigIntegerField(null=False)
    valid_id = models.BinaryField(null=True, blank=True, max_length=20)
    user_image = models.ImageField(null = True, blank = True)#models.BinaryField(null=True, blank=True)
    country = models.CharField(null=True, blank=True, max_length=20)
    current_location = models.CharField(null=True, blank=True, max_length=20)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

    def __str__(self):
        return f"info for: MR/MRS {self.user.first_name} {self.user.last_name} || email : {self.user.email}"