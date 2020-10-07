from django.contrib import admin
from .models import Todoapp

class Todoadmin(admin.ModelAdmin):
    readonly_fields = ('created_date', )

admin.site.register(Todoapp, Todoadmin)
 