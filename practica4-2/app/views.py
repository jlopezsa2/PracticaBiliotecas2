from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Library, Book, Loan, User
from django.db.models import Count

from .forms import LibraryForm, BookForm, UserForm, LoanForm, EditarLibroForm
from django.shortcuts import render, redirect

from django.shortcuts import get_object_or_404

from collections import defaultdict
from django.contrib import messages  # Si luego quieres mostrar mensajes





def lista_bibliotecas(request):
    bibliotecas = list(Library.objects.values("id","nombre", "direccion", "telefono"))
    return JsonResponse(bibliotecas, safe=False)

@csrf_exempt
def listar_registrar_biblioteca(request):
    if request.method == 'GET':
        bibliotecas = list(Library.objects.values("id","nombre", "direccion", "telefono"))
        return JsonResponse(bibliotecas, safe=False)
    
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            biblioteca = Library.objects.create(
                nombre=data['nombre'],
                telefono=data['telefono'],
                direccion=data['direccion']
            )
            return JsonResponse({"mensaje": "Biblioteca registrada con éxito", "biblioteca_id": biblioteca.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)




@csrf_exempt
def consultar_biblioteca(request, biblioteca_id):
    
    try:
        biblioteca = Library.objects.values("id","nombre", "direccion", "telefono").get(id=biblioteca_id)
        return JsonResponse(biblioteca)
    except Library.DoesNotExist:
        return JsonResponse({"error": "Biblioteca no registrada en el sistema"}, status=404)
    
@csrf_exempt    
def registrar_libro(request):
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            biblioteca = Library.objects.get(id=data['biblioteca_id'])
            nombreLibro = data['titulo']
            
            
            if data['titulo'] == "" or data['titulo'].strip() == "":
                return JsonResponse({"mensaje": "No puedes añadir un libro con titulo vacio"}, status=400)
            if Book.objects.filter(titulo=nombreLibro).exists():
                return JsonResponse({"mensaje": "El libro con ese titulo ya existe"}, status=400)
            
            
            
            libro = Book.objects.create(
                biblioteca = biblioteca,
                titulo=data['titulo'],
                autor=data['autor'],
                editorial=data['editorial']
            )
            
            return JsonResponse({"mensaje": "Libro registrado con éxito", "libro_id": libro.id})
        
        
            
        
        except Library.DoesNotExist:
            return JsonResponse({"error": "Biblioteca no registrada en el sistema"}, status=404)
        
        
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        
    return JsonResponse({"error": "Método no permitido"}, status=405)
 

@csrf_exempt
def listar_libros_de_biblioteca(request, biblioteca_id):
    try:
        libros = list(Book.objects.filter(biblioteca_id=biblioteca_id).values("id", "titulo", "autor", "editorial"))
        biblioteca = Library.objects.values("id","nombre", "direccion", "telefono").get(id=biblioteca_id)
        return JsonResponse(libros, safe=False)
    except Library.DoesNotExist:
        return JsonResponse({"error": "Biblioteca no existe"}, status=404)
    
@csrf_exempt    
def listar_modificar_borrar_libro(request, libro_id):
    if request.method == 'GET':     
        try:
            libro = Book.objects.values("id","titulo", "autor", "editorial", "biblioteca").get(id=libro_id)
            return JsonResponse(libro)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Libro no registrado en el sistema"}, status=404)
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            
            libro = Book.objects.get(id=libro_id)
            data = json.loads(request.body)
            libro.titulo = data.get('titulo', libro.titulo)  
            libro.autor = data.get('autor', libro.autor)
            libro.editorial = data.get('editorial', libro.editorial)
            biblioteca = Library.objects.values("id","nombre", "direccion", "telefono").get(id=data['biblioteca_id'])
            

            if 'biblioteca_id' in data:
                libro.biblioteca_id = data['biblioteca_id']
            
                libro.save()
            
            return JsonResponse({'Libro modificado con id:': libro.id})
            
            

        except Book.DoesNotExist:
            return JsonResponse({"error": "Libro no registrado en el sistema"}, status=404)

        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        
        except Library.DoesNotExist:
            return JsonResponse({"error": "Biblioteca no existe"}, status=400)
    
    
    if request.method == 'DELETE':     
        try:
            libro = Book.objects.get(id=libro_id)
            libro.delete()
            return JsonResponse({"message": "Libro ha sido borrado"})
        
        except Book.DoesNotExist:
            return JsonResponse({"error": "Libro no registrado en el sistema"}, status=404)
        
    
        
@csrf_exempt        
def listar_registrar_usuario(request):
    if request.method == 'GET':
        ususarios = list(User.objects.values("id","nombre", "email", "telefono"))
        return JsonResponse(ususarios, safe=False)
    
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ususario = User.objects.create(
                nombre=data['nombre'],
                email=data['email'],
                telefono=data['telefono']
            )
            return JsonResponse({"mensaje": "Usuario registrado con éxito", "usuario_id": ususario.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt 
def listar_usuario(request, usuario_id):
    
    if request.method == 'GET':     
        try:
            usuario = User.objects.values("id","nombre", "email", "telefono").get(id=usuario_id)
            return JsonResponse(usuario)
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no registrado en el sistema"}, status=404)
@csrf_exempt         
def listar_registrar_prestamos(request):
    if request.method == 'GET':     
    
        prestamos = list(Loan.objects.filter(devuelto=False)
                         .values("id", "usuario__nombre", "libro__titulo", "fecha", "devuelto"))
        return JsonResponse(prestamos, safe=False)
    
    if request.method == 'POST':     
        try:
            data = json.loads(request.body)
            libro = Book.objects.get(id=data['libro_id'])
            usuario = User.objects.get(id=data['usuario_id'])
            if Loan.objects.filter(libro=libro, devuelto=False).exists():
                return JsonResponse({"error": "El libro ya está prestado y no ha sido devuelto."}, status=400)
            prestamo = Loan.objects.create(
                libro = libro,
                usuario = usuario
            )
            return JsonResponse({"mensaje": "Prestamo registrado con éxito", "prestamo_id": prestamo.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Libro no registrado en el sistema"}, status=404)
        except User.DoesNotExist:
            return JsonResponse({"error": "usuario no registrado en el sistema"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)   

@csrf_exempt
def ver_prestamos_usuario(request, usuario_id):
    if request.method == 'GET':
        try:
            usuario = User.objects.values("id","nombre", "email", "telefono").get(id=usuario_id)
            prestamos = list(Loan.objects.filter(usuario_id=usuario_id).values("id", "usuario", "libro", "fecha", "devuelto"))
            return JsonResponse(prestamos, safe=False)
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)
        
@csrf_exempt
def devolver_libro(request, prestamo_id):
    if request.method == 'PUT':
        try:
            """data = json.loads(request.body)"""
            prestamo = Loan.objects.get(id=prestamo_id)
            if prestamo.devuelto == True:
                return JsonResponse({"error": "El préstamo ya ha sido devuelto."}, status=400)
            prestamo.devuelto = True  
            
            
            prestamo.save()
            
            return JsonResponse({'Prestamo devuelto con id:': prestamo_id})

        except Loan.DoesNotExist:
            return JsonResponse({"error": "Prestamo no registrado en el sistema"}, status=404)

        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)     
        
@csrf_exempt    
def libros_biblioteca_disponible(request, biblioteca_id):
        if request.method == 'GET':
            try:
            # Filtra los libros de la biblioteca
                libros = Book.objects.filter(biblioteca_id=biblioteca_id)
                biblioteca = Library.objects.values("id","nombre", "direccion", "telefono").get(id=biblioteca_id)

                libros_disponibles = libros.exclude(
                id__in=Loan.objects.filter(devuelto=False).values('libro_id')
                )

    
                libros_data = list(libros_disponibles.values("id", "titulo", "autor", "editorial"))
    
                return JsonResponse(libros_data, safe=False)

            except Library.DoesNotExist:
                return JsonResponse({"error": "Biblioteca no encontrada"}, status=404)
            
            
##############################################################################################################


def inicio(request):
    contexto = {'mensaje': '¡Bienvenido a la libreria!'}
    return render(request, 'inicio.html', contexto)



def nueva_biblioteca(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            form.full_clean()
            messages.success(request, 'Biblioteca añadida correctamente.')
            return redirect('inicio')
    else:
        form = LibraryForm()
    return render(request, 'formulario_biblioteca.html', {'form': form, 'titulo': 'Nueva Biblioteca'})


def ver_bibliotecas(request):
    bibliotecas = list(Library.objects.values("id","nombre", "direccion", "telefono").order_by("nombre"))
    return render(request, 'lista_bibliotecas.html', {'bibliotecas': bibliotecas})        



@csrf_exempt
def listar_libros_de_biblioteca_detalle(request, biblioteca_id):
    try:
        libros = list(Book.objects.filter(biblioteca_id=biblioteca_id).values("id", "titulo", "autor", "editorial"))
        biblioteca = Library.objects.values("id","nombre", "direccion", "telefono").get(id=biblioteca_id)
        return render(request, 'detalle_biblioteca.html', {
            'libros': libros,
            'biblioteca': biblioteca
        })
    except Library.DoesNotExist:
        return JsonResponse({"error": "Biblioteca no existe"}, status=404)
    
    
    
def nuevo_libro(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro añadido correctamente.')
            return redirect('inicio')
    else:
        form = BookForm()
    return render(request, 'formulario_libro.html', {'form': form, 'titulo': 'Nuevo Libro'})    


"""def ver_libros(request):
    libros = list(Book.objects.values("id","titulo", "autor", "editorial", "biblioteca").order_by("biblioteca"))
    return render(request, 'lista_libros.html', {'libros': libros}) """
    
def ver_libros(request):
    libros = Book.objects.select_related('biblioteca').all().order_by('biblioteca__nombre')
    
    libros_por_biblioteca = defaultdict(list)
    for libro in libros:
        libros_por_biblioteca[libro.biblioteca.nombre].append(libro)

    return render(request, 'lista_libros.html', {
        'libros_por_biblioteca': dict(libros_por_biblioteca)
    })



@csrf_exempt
def listar_libro(request, libro_id):
    try:
        libro = Book.objects.values("id", "titulo", "autor", "editorial", "biblioteca__nombre").get(id=libro_id)

        # Verificar si está prestado
        prestamo = Loan.objects.filter(libro_id=libro_id, devuelto=False).select_related("usuario").first()
        print(prestamo)
        return render(request, 'detalle_libro.html', {
            'libro': libro,
            'prestamo': prestamo })
        
    except Book.DoesNotExist:
        return JsonResponse({"error": "Libro no existe"}, status=404)
    
    
    
    
def editar_libro(request, libro_id):
    libro = get_object_or_404(Book, id=libro_id)
    
    if request.method == 'POST':
        form = EditarLibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Libro actualizado correctamente.')
            return redirect('listar_libro', libro_id=libro.id)
    else:
        form = BookForm(instance=libro)
    
    return render(request, 'actualizar_libro.html', {'form': form, 'libro': libro})



def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Book, id=libro_id)
    
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado correctamente.')
        return redirect('ver_libros') 

    return render(request, 'eliminar_libro.html', {'libro': libro})


@csrf_exempt        
def nuevo_usuario(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario añadido correctamente.')
            
    else:
        form = UserForm()
    return render(request, 'formulario_usuario.html', {'form': form, 'titulo': 'Nuevo Usuario'})    



@csrf_exempt 
def listar_usuarios(request):
    
    usuarios = list(User.objects.values("id","nombre", "email", "telefono"))
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})  



@csrf_exempt
def prestamos_usuario(request, usuario_id):
    if request.method == 'GET':
        try:
            usuario = User.objects.values("id","nombre", "email", "telefono").get(id=usuario_id)
            prestamos = list(Loan.objects.filter(usuario_id=usuario_id).values("id", "usuario__nombre", "libro__titulo", "fecha", "devuelto"))
            return render(request, 'detalle_usuario.html', {
            'usuario': usuario,
            'prestamos': prestamos
        })
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)

def nuevo_prestamo(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            libro = form.cleaned_data.get('libro')

            # Comprobamos si ya existe un préstamo activo para ese libro
            prestamo_existente = Loan.objects.filter(libro=libro, devuelto=False).exists()
            
            if prestamo_existente:
                messages.error(request, 'Este libro ya está prestado.')
            else:
                form.save()
                messages.success(request, 'Préstamo añadido correctamente.')
                return redirect('inicio')
    else:
        form = LoanForm()
    
    return render(request, 'formulario_prestamo.html', {'form': form, 'titulo': 'Nuevo Préstamo'})  
    
    

@csrf_exempt 
def listar_prestamos(request):
    
    prestamos = list(Loan.objects.filter(devuelto=False)
                    .values("id", "usuario__nombre", "libro__titulo", "fecha", "devuelto"))
    return render(request, 'lista_prestamos.html', {'prestamos': prestamos})  



def prestamos_por_usuario(request):
    
    usuarios = User.objects.all().prefetch_related('loan_set__libro')
    return render(request, 'historial_prestamos_usuario.html', {'usuarios': usuarios})



def devolver_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Loan, id=prestamo_id)
    if not prestamo.devuelto:
        prestamo.devuelto = True
        prestamo.save()
        messages.success(request, f'Préstamo del libro "{prestamo.libro.titulo}" marcado como devuelto.')
        return redirect('prestamos_por_usuario')  
    else:
        messages.info(request, 'Este préstamo ya estaba devuelto.')
    return redirect('prestamos_por_usuario')  