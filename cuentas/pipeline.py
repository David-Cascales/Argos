from cuentas.models import Rol

def asignar_rol_por_defecto(backend, user, response, *args, **kwargs):
    """
    Pipeline de OAuth2. Asigna el rol de 'usuario' por defecto a todo usuario que inicie
    sesión por primera vez con Google.
    """
    if user:
        if not user.rol:
            rol_usuario, _ = Rol.objects.get_or_create(nombre='usuario')
            user.rol = rol_usuario

        if not user.nombre or user.nombre == user.email.split('@')[0]:
            nombre_google = response.get('name', '')
            if nombre_google:
                user.nombre = nombre_google

        user.save()