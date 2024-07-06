from django.contrib import admin

from .models import Vacancy

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'city', 'description', 'gender', 'children',\
                    'education', 'profession', 'alcohol', 'smoke', 'horoscope', 'target')
    fields = ('name', 'age', 'city', 'description', 'gender', 'children', 'images',\
                    'education', 'profession', 'alcohol', 'smoke', 'horoscope', 'target', 'advuser')

class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'employer', 'salary', 'employment', 'experience', 'area', 'profRole')

admin.site.register(Vacancy, VacancyAdmin)