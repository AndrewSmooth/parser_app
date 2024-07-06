from tabnanny import verbose
from django.db import models

# Create your models here
class Vacancy(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название вакансии')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Адрес')
    employer = models.CharField(max_length=200, verbose_name='Работодатель')
    salary = models.CharField(max_length=200, blank=True, null=True, verbose_name='Зарплата')
    employment = models.CharField(max_length=180, verbose_name='Занятость')
    experience = models.CharField(max_length=180, verbose_name='Опыт работы')
    area = models.CharField(max_length=200, verbose_name='Регион')
    profRole = models.CharField(max_length=200, verbose_name='Специальность')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'