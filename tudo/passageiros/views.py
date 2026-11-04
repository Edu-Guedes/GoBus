from datetime import date, timedelta
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from urllib.parse import urlencode
from .models import Passageiro

# Create your views here.

# ---------- PERFIL ----------
# get_object_or_404: função do Django que procura um registro no banco de dados.
# Passageiro: modelo que representa a tabela de passageiros.
def perfil_view(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)
    contexto = {"aba": "perfil", "passageiro": passageiro}
    return render(request, "passageiros/perfil.html", contexto)


def meus_dados_view(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)
    contexto = {"aba": "perfil", "titulo": "Meus dados", "voltar": "passageiros:perfil", "passageiro": passageiro}
    return render(request, "passageiros/meus_dados.html", contexto)


def enderecos_view(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)
    contexto = {
        "aba": "perfil", 
        "titulo": "Endereços", 
        "voltar": "passageiros:perfil", 
        "passageiro": passageiro,
    }
    return render(request, "passageiros/enderecos.html", contexto)


def historico_view(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)
    contexto = {
        "aba": "perfil",
        "titulo": "Histórico de viagens",
        "voltar": "passageiros:perfil",
        "passageiro": passageiro,
        "registros": passageiro.frequencias.all(),
    }
    return render(request, "passageiros/historico.html", contexto)


def configuracoes_view(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)
    contexto = {"aba": "perfil", "titulo": "Configurações", "voltar": "passageiros:perfil", "passageiro": passageiro}
    return render(request, "passageiros/configuracoes.html", contexto)


def ajuda_view(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)
    contexto = {"aba": "perfil", "titulo": "Ajuda e suporte", "voltar": "passageiros:perfil", "passageiro": passageiro}
    return render(request, "passageiros/ajuda.html", contexto)

