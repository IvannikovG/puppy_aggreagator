from django.contrib import admin
from . import models


class AnimalAdmin(admin.ModelAdmin):
    list_display = ('animal_name', 'species')


admin.site.register(models.Animal, AnimalAdmin)
