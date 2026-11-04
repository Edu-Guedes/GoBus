from django.db import models
from django.utils import timezone


class Passageiro(models.Model):
    """Perfil do passageiro. É cadastrado pelo painel /admin/."""
    VINCULOS = [("estudante", "Estudante"), ("trabalhador", "Trabalhador")]
    SITUACOES = [("pendente", "Pendente"), ("aprovado", "Aprovado"), ("rejeitado", "Rejeitado")]

    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14)
    idade = models.PositiveIntegerField()
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    endereco = models.CharField(max_length=200)
    vinculo = models.CharField(max_length=12, choices=VINCULOS, default="estudante")
    situacao = models.CharField(max_length=10, choices=SITUACOES, default="aprovado")

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Frequencia(models.Model):
    """Histórico: dia em que o passageiro registrou ida ou volta. Cancelar = apagar o registro."""
    TIPOS = [("ida", "Ida"), ("volta", "Volta")]

    passageiro = models.ForeignKey(Passageiro, on_delete=models.CASCADE, related_name="frequencias")  # 1:N
    data = models.DateField()
    tipo = models.CharField(max_length=5, choices=TIPOS)

    class Meta:
        ordering = ["-data", "tipo"]
        unique_together = ("passageiro", "data", "tipo")

    def __str__(self):
        return f"{self.passageiro} · {self.data:%d/%m/%Y} · {self.get_tipo_display()}"



class Notificacao(models.Model):
    """Aviso mostrado na tela de notificações do passageiro. É cadastrado pelo painel /admin/."""
    TIPOS = [("alerta", "Alerta"), ("aviso", "Aviso"), ("info", "Informação")]
    ICONES = {"alerta": "⚠️", "aviso": "ℹ️", "info": "📄"}

    passageiro = models.ForeignKey(Passageiro, on_delete=models.CASCADE, related_name="notificacoes")
    tipo = models.CharField(max_length=6, choices=TIPOS, default="aviso")
    titulo = models.CharField(max_length=100)
    mensagem = models.TextField()
    criada_em = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-criada_em"]
        verbose_name = "notificação"
        verbose_name_plural = "notificações"

    def __str__(self):
        return f"{self.passageiro} · {self.titulo}"

    @property
    def icone(self):
        return self.ICONES.get(self.tipo, "ℹ️")

    @property
    def tempo_curto(self):
        """Tempo desde que foi criada, no formato curto: 0m, 6m, 2h, 3d."""
        minutos = max(int((timezone.now() - self.criada_em).total_seconds() // 60), 0)
        if minutos < 60:
            return f"{minutos}m"
        horas = minutos // 60
        if horas < 24:
            return f"{horas}h"
        return f"{horas // 24}d"