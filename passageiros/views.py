"""Views do passageiro (uma por tela). O passageiro vem do id na URL."""
from datetime import date, timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from urllib.parse import urlencode

from .models import Frequencia, Passageiro


def _converter_data(texto):
    """Converte 'AAAA-MM-DD' em data. Se for inválido, usa hoje."""
    try:
        return date.fromisoformat(texto)
    except (TypeError, ValueError):
        return timezone.localdate()


# ---------- INÍCIO ----------
"""Views do passageiro (uma por tela). O passageiro vem do id na URL."""
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Frequencia, Passageiro


# ---------- INÍCIO (inclui marcar ida e volta) ----------
def inicio_view(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)
    hoje = timezone.localdate()

    # Clicou em Confirmar ou Cancelar (ida/volta de hoje)
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        acao = request.POST.get("acao")

        if tipo in ("ida", "volta"):
            if acao == "confirmar":
                Frequencia.objects.get_or_create(passageiro=passageiro, data=hoje, tipo=tipo)
            elif acao == "cancelar":
                Frequencia.objects.filter(passageiro=passageiro, data=hoje, tipo=tipo).delete()

        return redirect("passageiros:inicio", passageiro_id=passageiro.id)

    marcados = passageiro.frequencias.filter(data=hoje)
    contexto = {
        "aba": "inicio",
        "kicker": "BEM-VINDO",
        "titulo": f"Olá, {passageiro.nome}! 👋",
        "passageiro": passageiro,
        "marcados": marcados,
        "ida_ok": marcados.filter(tipo="ida").exists(),
        "volta_ok": marcados.filter(tipo="volta").exists(),
    }
    return render(request, "passageiros/inicio.html", contexto)


# ---------- IDA E VOLTA ----------
def ida_volta_view(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)

    # Clicou em Confirmar ou Cancelar
    if request.method == "POST":
        dia = _converter_data(request.POST.get("data"))
        tipo = request.POST.get("tipo")
        acao = request.POST.get("acao")

        if tipo in ("ida", "volta"):
            if acao == "confirmar":
                Frequencia.objects.get_or_create(passageiro=passageiro, data=dia, tipo=tipo)
            elif acao == "cancelar":
                Frequencia.objects.filter(passageiro=passageiro, data=dia, tipo=tipo).delete()

        url = reverse("passageiros:ida_volta", args=[passageiro.id])
        return redirect(f"{url}?d={dia.isoformat()}")

    # Mostrar a tela: dia escolhido (?d=2026-11-03) e os 5 dias da semana
    dia = _converter_data(request.GET.get("d"))
    segunda = dia - timedelta(days=dia.weekday())
    dias = [segunda + timedelta(days=i) for i in range(5)]

    contexto = {
        "aba": "ida_volta",
        "titulo": "Ida e Volta (Diária)",
        "voltar": "passageiros:inicio",
        "passageiro": passageiro,
        "dia": dia,
        "dias": dias,
        "ida_ok": passageiro.frequencias.filter(data=dia, tipo="ida").exists(),
        "volta_ok": passageiro.frequencias.filter(data=dia, tipo="volta").exists(),
    }
    return render(request, "passageiros/ida_volta.html", contexto)


# ---------- PERFIL ----------
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
    contexto = {"aba": "perfil", "titulo": "Endereços", "voltar": "passageiros:perfil", "passageiro": passageiro}
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


# ---------- ROTAS (mapa) ----------
# Trocar pelos endereços reais da linha (ou, no futuro, buscar de um model Rota).
ROTA_ORIGEM = "Praça da Sé, São Paulo - SP"
ROTA_DESTINO = "Avenida Paulista, 1578, São Paulo - SP"


def rota_view(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)

    # Mapa embutido (iframe) com o trajeto desenhado entre origem e destino
    mapa_url = "https://maps.google.com/maps?" + urlencode(
        {"saddr": ROTA_ORIGEM, "daddr": ROTA_DESTINO, "output": "embed", "hl": "pt-BR"}
    )
    # Mesmo trajeto, para abrir no app/site do Google Maps
    mapa_externo = "https://www.google.com/maps/dir/?" + urlencode(
        {"api": 1, "origin": ROTA_ORIGEM, "destination": ROTA_DESTINO}
    )

    contexto = {
        "aba": "rotas",
        "titulo": "Rota em tempo real",
        "voltar": "passageiros:inicio",
        "centralizar": True,
        "passageiro": passageiro,
        "mapa_url": mapa_url,
        "mapa_externo": mapa_externo,
        # Dados de exemplo (ainda sem GPS real)
        "rota": {
            "linha": "Centro → Escola Estadual",
            "motorista": "Carlos Silva",
            "velocidade": "32 km/h",
            "proxima_parada": "3 min",
        },
    }
    return render(request, "passageiros/rota.html", contexto)


# ---------- NOTIFICAÇÕES ----------
FILTROS_NOTIFICACAO = {
    "todas": None,                    # sem filtro
    "avisos": ("aviso", "info"),
    "alertas": ("alerta",),
}


def notificacoes_view(request, passageiro_id):
    passageiro = get_object_or_404(Passageiro, id=passageiro_id)

    # Aba escolhida (?tipo=avisos). Se vier algo inválido, mostra todas.
    filtro = request.GET.get("tipo", "todas")
    if filtro not in FILTROS_NOTIFICACAO:
        filtro = "todas"

    notificacoes = passageiro.notificacoes.all()
    if FILTROS_NOTIFICACAO[filtro]:
        notificacoes = notificacoes.filter(tipo__in=FILTROS_NOTIFICACAO[filtro])

    contexto = {
        "aba": "notificacoes",
        "titulo": "Notificações",
        "voltar": "passageiros:inicio",
        "centralizar": True,
        "passageiro": passageiro,
        "filtro": filtro,
        "notificacoes": notificacoes,
    }
    return render(request, "passageiros/notificacoes.html", contexto)

