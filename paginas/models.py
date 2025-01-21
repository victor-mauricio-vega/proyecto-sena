from django.db import models

# Create your models here.
class Estado(models.Model):
    id_estado=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=30)

class Categoria(models.Model):
    id_categoria=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=30)

class Rol(models.Model):
    id_rol=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=30)

class Vendedor(models.Model):
    identificacion=models.IntegerField(primary_key=True,)
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)
    telefono=models.IntegerField()
    correo=models.CharField(max_length=30)
    id_rol=models.ForeignKey(Rol, on_delete=models.CASCADE)
    contrasena=models.CharField(max_length=130)

class Automovil(models.Model):
    id_auto=models.AutoField(primary_key=True)
    modelo=models.IntegerField()
    marca=models.CharField(max_length=30)
    color=models.CharField(max_length=30)
    placa=models.CharField(max_length=10)
    precio=models.IntegerField(default=00)
    imagen=models.ImageField(upload_to='imagenes')
    id_estado=models.ForeignKey(Estado, on_delete=models.CASCADE)
    id_categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)
    identificacion=models.ForeignKey(Vendedor,on_delete=models.CASCADE)

