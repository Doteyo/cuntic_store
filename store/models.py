from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Cunty(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    price = models.IntegerField("Цена", default=0)
    name = models.CharField("Название", max_length=30, default="")
    color = models.CharField("Цвет", max_length=30, default="")
    size = models.CharField("Размер", max_length=3, default="")
    weight = models.IntegerField("Вес", default=0)
    materials = models.CharField("Материалы", max_length=45, default="")
    add_features = models.TextField("Дополнительные свойства", max_length=120, default="")
    status = models.IntegerField("Статус", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кунтик"
        verbose_name_plural = "Кунтики"


class Room(models.Model):
    name = models.CharField(max_length=1000)


class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
