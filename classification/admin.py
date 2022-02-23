from django.contrib import admin

from .models import Nomenclature

# Register your models here.
@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = ('code', 'nomenclature', 'units', 'group', 'nomenclature_group', 'nomenclature_group_detail', 'brand', 'actual')