from django.urls import path
from .views import(
    listar_registrar_biblioteca, consultar_biblioteca, 
    registrar_libro, listar_libros_de_biblioteca, listar_modificar_borrar_libro, listar_registrar_usuario,listar_registrar_prestamos,
    listar_usuario, ver_prestamos_usuario, devolver_libro, libros_biblioteca_disponible,
    nueva_biblioteca,inicio, ver_bibliotecas, listar_libros_de_biblioteca_detalle, nuevo_libro, ver_libros, listar_libro, editar_libro,
    eliminar_libro, nuevo_usuario, listar_usuarios, prestamos_usuario, nuevo_prestamo, listar_prestamos, prestamos_por_usuario, devolver_prestamo
    
)

urlpatterns = [
    
    path('libraries/', listar_registrar_biblioteca, name='lista_bibliotecas'), #name=listar_registrarlista_biblioteca
    path('libraries/<int:biblioteca_id>/', consultar_biblioteca, name='consultar_biblioteca'),
    path('books/', registrar_libro, name='registrar_libro'),
    path('libraries/<int:biblioteca_id>/books/', listar_libros_de_biblioteca, name='listar_libros_de_biblioteca'),
    path('books/<int:libro_id>', listar_modificar_borrar_libro, name='listar_modificar_borrar_libro'),
    path('users/', listar_registrar_usuario, name='listar_registrar_usuario'),
    path('users/<int:usuario_id>', listar_usuario, name='listar_usuario'),
    path('loans/', listar_registrar_prestamos, name='listar_registrar_prestamos'),
    path('users/<int:usuario_id>/loans/', ver_prestamos_usuario, name='ver_prestamos_usuario'),
    path('loans/<int:prestamo_id>/', devolver_libro, name='devolver_libro'),
    path('books/<int:biblioteca_id>/avaliable/', libros_biblioteca_disponible, name='libros_biblioteca_disponible'),
    path('', inicio, name='inicio'),
    path('bibliotecas/nueva/', nueva_biblioteca , name='nueva_biblioteca'),
    path('bibliotecas/', ver_bibliotecas , name='ver_bibliotecas'),
    path('bibliotecas/<int:biblioteca_id>/books/', listar_libros_de_biblioteca_detalle , name='listar_libros_de_biblioteca_detalle'),
    path('libros/nuevo/', nuevo_libro , name='nuevo_libro'),
    path('libros/', ver_libros , name='ver_libros'),
    path('libro/<int:libro_id>', listar_libro , name='listar_libro'),
    path('libro/<int:libro_id>/editar/', editar_libro, name='editar_libro'),
    path('libro/<int:libro_id>/eliminar/', eliminar_libro, name='eliminar_libro'),
    path('usuario/nuevo/', nuevo_usuario , name='nuevo_usuario'),
    path('usuarios/', listar_usuarios , name='listar_usuarios'),
    path('usuarios/<int:usuario_id>/prestamos/', prestamos_usuario, name='prestamos_usuario'),
    path('prestamo/nuevo/', nuevo_prestamo , name='nuevo_prestamo'),
    path('prestamos/', listar_prestamos , name='listar_prestamos'),
    path('prestamos/activos', prestamos_por_usuario , name='prestamos_por_usuario'),
    path('prestamo/<int:prestamo_id>/devolver/', devolver_prestamo, name='devolver_prestamo'),
    
    
     
]




