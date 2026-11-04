from django.urls import path
from . import views

app_name = "passageiros"

urlpatterns = [
    path("passageiro/<int:passageiro_id>/perfil/", views.perfil_view, name="perfil"),
    path("passageiro/<int:passageiro_id>/perfil/meus-dados/", views.meus_dados_view, name="meus_dados"),
    path("passageiro/<int:passageiro_id>/perfil/enderecos/", views.enderecos_view, name="enderecos"),
    path("passageiro/<int:passageiro_id>/perfil/historico/", views.historico_view, name="historico"),
    path("passageiro/<int:passageiro_id>/perfil/configuracoes/", views.configuracoes_view, name="configuracoes"),
    path("passageiro/<int:passageiro_id>/perfil/ajuda/", views.ajuda_view, name="ajuda"),
]
