from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.inicio,name='inicio'),
    path('vehiculos',views.vehiculos,name='vehiculos'),
    path('login',views.iniciar,name='login'),
    path('salir',views.salir, name='salir'),
    path('registro',views.registro,name='registro'),
    path('listar_info/<int:id>',views.listar_info,name='listar_info'),
    path('lista_vendedor<int:id>',views.lista_vendedor,name='lista_vendedor'),
    path('editar_perfil',views.editar_perfil,name='editar_perfil'),
    
    


    path('listar_usuario',views.listar_usuario,name='listar_usuario'),
    
    # VENDEDORES
    path('registro_vendedor',views.registro_vendedor,name='registro_vendedor'),
    path('listar_vendedor',views.listar_vendedor,name='listar_vendedor'),
    path('actualizar_vendedor<int:id>',views.actualizar_vendedor,name='actualizar_vendedor'),
    path('eliminar_vendedor<int:id>',views.eliminar_vendedor,name='eliminar_vendedor'),
    
    #AUTOMOVILES
    path('registrar_auto',views.registrar_auto,name='registrar_auto'),
    path('listar_auto',views.listar_auto,name='listar_auto'),
    path('actualizar_auto<int:id>',views.actualizar_auto, name='actualizar_auto'),
    path('eliminar_auto<int:id>',views.eliminar_auto,name='eliminar_auto'),

    #ADMINISTRADOR 
    path('administrador',views.administrador,name='administrador'),
    path('categoria',views.categoria, name='categoria'),
    path('estado',views.estado, name='estado'),
    path('rol',views.rol, name='rol'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)