from django.contrib import admin
from .models import Entrie


@admin.register(Entrie)
class EntrieAdmin(admin.ModelAdmin):
    pass
