from django.contrib import admin

from donation.models import Institution


# Register your models here.
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type')
    search_fields = ('name', 'description')
    list_filter = ('type',)