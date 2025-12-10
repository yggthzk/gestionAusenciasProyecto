from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SolicitudAusencia(models.Model):
    DEPARTAMENTOS = [
        ('rrhh', 'Recursos Humanos'),
        ('it', 'Tecnología'),
        ('finanzas', 'Finanzas'),
        ('operaciones', 'Operaciones'),
        ('ventas', 'Ventas'),
        ('OTROS DEPARTAMENTOS', 'Sin departamento') # da error 01/12
    ]

    TIPOS_AUSENCIA = [
        ('vacaciones', 'Vacaciones'),
        ('enfermedad', 'Baja Médica'),
        ('asuntos_personales', 'Asuntos Personales'),
        ('administrativo', 'Trámite Administrativo'),
    ]

    ESTADOS = [
        ('pendiente', 'Pendiente de Aprobación'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes')
    codigo_empleado = models.CharField(max_length=20, unique=True)
    nombre_completo = models.CharField(max_length=200)
    departamento = models.CharField(max_length=50, choices=DEPARTAMENTOS)
    puesto_trabajo = models.CharField(max_length=100)
    supervisor_directo = models.CharField(max_length=200)
    
    tipo_ausencia = models.CharField(max_length=30, choices=TIPOS_AUSENCIA, default='vacaciones')
    fecha_ausencia = models.DateField()
    motivo_detallado = models.TextField()
    
    correo_contacto = models.EmailField()
    telefono_contacto = models.CharField(max_length=20)
    telefono_emergencia = models.CharField(max_length=20)
    
    estado = models.CharField(max_length=30, choices=ESTADOS, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo_empleado} - {self.fecha_ausencia}"

    def clean(self):
        dias_usados = SolicitudAusencia.objects.filter(
            usuario=self.usuario, 
            estado='aprobada'
        ).exclude(id=self.id).count()

        if dias_usados >= 2 and self.estado == 'aprobada':
            raise ValidationError("Límite de ausencias anuales excedido.")