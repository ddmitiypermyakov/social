from django.db import models
from django.core.validators import *
from django.contrib.auth.models import AbstractUser

# Create your models here.
# telephone = RegexValidator(r'^\d+$', 'Only numeric characters are allowed.')

class Person(AbstractUser):
    # name = models.CharField(max_length=150, verbose_name='Имя', db_index=True)
    # last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    phone = models.PositiveIntegerField(null=True, blank=True,verbose_name='Телефон')
    # email = models.EmailField(verbose_name='Электронная почта')
    city = models.ForeignKey('City',null=True, on_delete=models.CASCADE, verbose_name='Город')
    photo = models.ImageField(upload_to='image/%Y/%m/%d/', verbose_name='Фото')
    birthday = models.DateField(null=True, blank=True, verbose_name='Дата Рождения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE, null=True, verbose_name='Пол')
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию')
    send_messages = models.BooleanField(default=True, verbose_name='Слать оповещения о новых комментариях?')

    class Meta(AbstractUser.Meta):
        pass

# class Person(models.Model):
#     name = models.CharField(max_length=150, verbose_name='Имя', db_index=True)
#     last_name = models.CharField(max_length=150, verbose_name='Фамилия')
#     phone = models.PositiveIntegerField(validators=[telephone, MaxLengthValidator],
#                                         verbose_name='Телефон')
#     email = models.EmailField(verbose_name='Электронная почта')
#     city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
#     photo = models.ImageField(upload_to='image/%Y/%m/%d/', verbose_name='Фото')
#     birthday = models.DateField(verbose_name='Дата Рождения')
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
#     gender = models.ForeignKey('Gender', on_delete=models.CASCADE, null=True, verbose_name='Пол')
#
#     def __str__(self):
#         return f'{self.name} {self.last_name}'






class Gender(models.Model):
    # KINDS = (
    #     ('None', 'Выберите пол'),
    #     ('male', 'Мужчина'),
    #     ('female', 'Женщина'),
    #
    # )
    gender = models.CharField(max_length=10, blank=True, verbose_name='Пол' )#choices=KINDS

    def __str__(self):
        return self.gender


class City(models.Model):
    city = models.CharField(null=True,max_length=100, blank=True, verbose_name='Город')

    def __str__(self):
        return self.city
