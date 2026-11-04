from django.db import models

# Create your models here.

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

    # passageiros apresentados em ordem pelo nome
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
