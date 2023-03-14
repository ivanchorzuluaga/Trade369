from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    Administrador = models.BooleanField('Administrador' , default=False)
    inversor = models.BooleanField('Inversor',default=True)

    class Meta:
        ordering = ('username',)

class cliente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30,blank=True)
    correo = models.EmailField(max_length=60)
    telefono = models.BigIntegerField()
    creacion = models.DateField(auto_now_add=True)
    estado = models.BooleanField(default=False)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ('nombre',)

class contrato(models.Model):
    NomCliente = models.ForeignKey(cliente, on_delete=models.CASCADE)
    inversion = models.BigIntegerField()
    fechaIncio = models.DateField()
    fechaFin = models.DateField(null=True, blank=True)
    usuarioC = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.NomCliente.nombre
    
    class Meta:
        ordering = ('NomCliente',)

class valores(models.Model):
    contrato = models.ForeignKey(contrato, on_delete=models.CASCADE)
    interesDia = models.CharField(max_length=10)
    fechaDia = models.DateField()
    SubTotal = models.BigIntegerField()
    usuarioV = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.contrato.NomCliente.nombre
    
    class Meta:
        ordering = ('fechaDia',)

class retiro(models.Model):
    contrato = models.ForeignKey(contrato, on_delete=models.CASCADE)
    fechaRetiro = models.DateField()
    valorRetiro = models.CharField(max_length=100)

    def __str__(self):
        return self.contrato.NomCliente.nombre
    
    class Meta:
        ordering = ('contrato',)