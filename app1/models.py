from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Userinfo(AbstractUser):
    tel = models.CharField(max_length=32,blank=True,null=True)
    address = models.CharField(max_length=100,blank=True,null=True)
    gender = models.IntegerField(choices=((1,"男"),(2,"女")),default=1)

    def __str__(self):
        return self.username


class Order(models.Model):
    order_num = models.CharField(max_length=30,blank=True,null=True)
    date = models.CharField(max_length=30,blank=True,null=True)
    user = models.ForeignKey("Userinfo",on_delete=models.CASCADE)
    sum_price = models.CharField(max_length=20,blank=True,null=True)
    goods = models.ManyToManyField("Shangpin", related_name="good", blank=True)
    details = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=((1,"未付款"),(2,"已付款")),default=1)

    def get_status(self):
        return self.get_status_display()

class Shangpin(models.Model):
    image_path = models.CharField(max_length=100,blank=True,null=True)
    catagory = models.IntegerField(choices=((1,"吃的"),(2,"喝的"),(3,"玩的")))
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=100,blank=True,null=True)
    details = models.TextField(null=True,blank=True)

