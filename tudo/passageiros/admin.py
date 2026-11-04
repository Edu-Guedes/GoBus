from django.contrib import admin
from .models import Frequencia, Passageiro

# Register your models here.

# em PassageiroAdmin:

class FrequenciaInline(admin.TabularInline):
    model = Frequencia
    extra = 0


@admin.register(Passageiro)
class PassageiroAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "vinculo", "situacao")
    list_filter = ("vinculo", "situacao")
    search_fields = ("nome", "cpf")
    inlines = [FrequenciaInline]

