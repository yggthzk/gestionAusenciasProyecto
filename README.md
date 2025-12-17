# gestionAusenciasProyecto
Esta app de gestion de ausencias es util para administrar la solicitud, aprobacion o rechazo de solicitudes de ausencias a los usuarios(empleados)  mediante una GUI simple  facilitando la gestion de reemplazos 

Los Empleados y Administradores acceden usando el mismo inicio de sesion, Las cuentas posee



COMANDO PARA CREAR EMPLEADOS SIN ROLES

from django.contrib.auth.models import User
user = User.objects.create_user('empleado1', 'correo@empresa.com', '1234')
user.first_name = "Juan"
user.last_name = "Perez"
user.save()
exit()