from django.contrib import admin

from .models import Frequencia, Passageiro, Notificacao


class NotificacaoInline(admin.TabularInline):
    model = Notificacao
    extra = 0

# em PassageiroAdmin:


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "passageiro", "tipo", "criada_em")
    list_filter = ("tipo",)
    search_fields = ("titulo", "passageiro__nome")


class FrequenciaInline(admin.TabularInline):
    model = Frequencia
    extra = 0


@admin.register(Passageiro)
class PassageiroAdmin(admin.ModelAdmin):
    list_display = ("nome", "cpf", "vinculo", "situacao")
    list_filter = ("vinculo", "situacao")
    search_fields = ("nome", "cpf")
    inlines = [FrequenciaInline]


@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ("passageiro", "data", "tipo")
    list_filter = ("tipo", "data")



inlines = [FrequenciaInline, NotificacaoInline]