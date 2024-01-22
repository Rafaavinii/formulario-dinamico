import json
from django.db import models
from django.contrib.auth.models import User

class FormDinamico(models.Model):
    nome = models.CharField(max_length=60)
    descricao = models.CharField(max_length=500)
    data_criacao = models.DateField()
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class Questao(models.Model):

    TIPOS_DE_QUESTAO = [
        ('escolha_unica', 'Escolha Única'),
        ('multipla_escolha', 'Escolha Múltipla'),
        ('texto', 'Texto'),
        ('true_false', 'Verdadeiro ou Falso'),
        ('data', 'Data'),
        ('numero', 'Número'),
    ]

    questao_texto = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPOS_DE_QUESTAO)
    formulario = models.ForeignKey(FormDinamico, on_delete=models.CASCADE)
    itens = models.JSONField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.questao_texto
    
class Resposta(models.Model):
    resposta_texto = models.CharField(max_length=255)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    data_resposta = models.DateField()
    hora = models.TimeField()
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.resposta_texto
    
