from django.shortcuts import render
from tudo.passageiros.models import Passageiro

# Create your views here.

def inicio_view(request):
    """Tela inicial: lista os passageiros cadastrados no admin para escolher qual abrir."""
    contexto = {
        "kicker": "BEM-VINDO",
        "titulo": "GoBus",
        "passageiros": Passageiro.objects.all(),
    }
    return render(request, "core/inicio.html", contexto)
