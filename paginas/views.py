from django.contrib import messages
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,make_password





# Create your views here.
def inicio(request):
    return render(request,'paginas/index.html')

def salir(request):
    logout(request)
    messages.info(request,'la sesion fue cerrada!!')
    return redirect('inicio')

def iniciar(request):
    if request.user.is_authenticated:   
        return redirect('inicio')

    if request.method == 'POST':
        identificacion = request.POST.get('identificacion')
        password = request.POST.get('password')

        user = authenticate(request, username=identificacion, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {} {}'.format(user.first_name, user.last_name))
            return redirect('vehiculos')

        
        vendedor = authenticate_vendedor(request, identificacion, password)
        if vendedor:
            messages.success(request, 'Bienvenido {} {}'.format(vendedor.nombre, vendedor.apellido))
            return redirect('listar_usuario') 
        messages.error(request, 'Usuario o contraseña no válidos')

    return render(request, 'usuarios/login.html')

def registro(request):
    form = registroForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method =='POST':
        
        if form.is_valid():
            user = form.save()
            if user:
                messages.success(request, 'Usuario registrado exitosamente')
                return redirect('inicio')
        else:
            print("Formulario inválido. Errores:", form.errors)  
    else:
        return render(request, 'usuarios/registro.html', {'form': form})

def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Se guardaron los cambios exitosamente')
            return redirect('inicio')
    else:
        form = EditarPerfilForm(instance=request.user)
    return render(request, 'paginas/editar_perfil.html', {'form': form})

def listar_usuario(request):
    users=User.objects.all()

    data={
        'users':users
    }
    return render(request,'paginas/usuarios.html',data)

def authenticate_vendedor(request, identificacion, contrasena):
    try:
        vendedor = Vendedor.objects.get(identificacion=identificacion)
        if check_password(contrasena, vendedor.contrasena):   
            return vendedor
            
    except Vendedor.DoesNotExist:
      return None

def registro_vendedor(request):
    if request.method=='POST':
        identificacion=request.POST.get('identificacion')
        nombre=request.POST.get('nombre').capitalize()
        apellido=request.POST.get('apellido').capitalize()
        telefono=request.POST.get('telefono')
        correo=request.POST.get('correo')
        cargo=request.POST.get('id_rol')
        contrasena=request.POST.get('contrasena')

        contrasena_hasheada=make_password(contrasena)

        
        vendedor=Vendedor(
            identificacion=identificacion,
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            correo=correo,
            id_rol=Rol.objects.get(id_rol=cargo),
            contrasena=contrasena_hasheada
        )
        if Vendedor.objects.filter(identificacion=identificacion).exists():
            messages.error(request,'Numero Identificacion fue registrada anteriormente')
            return redirect('listar_vendedor')
        if Vendedor.objects.filter(correo=correo).exists():
            messages.error(request,'El correo '+correo+' fue registrado anteriormente')
            return redirect('listar_vendedor')
        vendedor.save()
        messages.success(request,'Registro exitoso')
        return redirect('listar_vendedor')

def listar_vendedor(request):
    vendedores=Vendedor.objects.all()
    cargos=Rol.objects.all()
    data={
        'vendedores':vendedores,
        'cargos':cargos
    }
    return render(request,'paginas/vendedores.html',data)

def lista_vendedor(request,id):
    if request.method == 'POST':
        vendedor=Vendedor.objects.get(identificacion=id)
        vendedor.nombre=request.POST.get('nombre').capitalize()
        vendedor.apellido=request.POST.get('apellido').capitalize()
        vendedor.telefono=request.POST.get('telefono')
        vendedor.correo=request.POST.get('correo')
        id_rol=request.POST.get('id_rol')
        
        cargo=Rol.objects.get(id_rol=id_rol)
        vendedor.id_rol=cargo

        vendedor.save()            
    return redirect('listar_info')

def listar_info(request, marca):
    try:
        auto = Automovil.objects.get(marca=marca)
        vendedor = auto.identificacion
        if vendedor:
            
            identificacion = vendedor.identificacion
            nombre = vendedor.nombre
            apellido = vendedor.apellido
            telefono = vendedor.telefono
            correo = vendedor.correo
        data = {
            'auto': auto,
            'vendedor': vendedor,    
        }
        return render(request, 'paginas/lista_vendedor.html', data)
    except Automovil.DoesNotExist:
        return render(request, 'paginas/lista_vendedor.html', {'auto': None, 'vendedor': None})

def actualizar_vendedor(request,id):
    if request.method == 'POST':
        vendedor=Vendedor.objects.get(identificacion=id)
        vendedor.nombre=request.POST.get('nombre').capitalize()
        vendedor.apellido=request.POST.get('apellido').capitalize()
        vendedor.telefono=request.POST.get('telefono')
        vendedor.correo=request.POST.get('correo')
        id_rol=request.POST.get('id_rol')
        
        cargo=Rol.objects.get(id_rol=id_rol)
        vendedor.id_rol=cargo

        nuevo_correo=request.POST.get('correo')
        if Vendedor.objects.exclude(identificacion=id).filter(correo=nuevo_correo).exists():
            messages.error(request,'El correo '+nuevo_correo+' fue registrado anteriormente')
        else:
            vendedor.correo=nuevo_correo
            vendedor.save()
            messages.success(request,'Se actualizaron los datos del vendedor')
    return redirect('listar_vendedor')

def eliminar_vendedor(request,id):
    vendedor=Vendedor.objects.get(identificacion=id)
    vendedor.delete()
    messages.success(request, 'Se elimino correctamente')
    return redirect('listar_vendedor')

def listar_auto(request):
    autos=Automovil.objects.all()
    estados=Estado.objects.all()
    vendedores=Vendedor.objects.all()
    categorias=Categoria.objects.all()

    data={
        'autos':autos,
        'estados':estados,
        'vendedores':vendedores,
        'categorias':categorias,
    }
    return render(request,'paginas/auto.html', data)

def registrar_auto(request):
    if request.method =='POST':
        modelo=request.POST.get('modelo')
        marca=request.POST.get('marca').capitalize()
        color=request.POST.get('color').capitalize()
        placa=request.POST.get('placa')
        precio=request.POST.get('precio')
        imagen=request.FILES.get('imagen')
        estado=request.POST.get('id_estado')
        categoria=request.POST.get('id_categoria')
        vendedor=request.POST.get('identificacion')


        auto=Automovil(
            modelo=modelo,
            marca=marca,
            color=color,
            placa=placa,
            precio=precio,
            imagen=imagen,
            id_estado=Estado.objects.get(id_estado=estado),
            id_categoria=Categoria.objects.get(id_categoria=categoria),
            identificacion=Vendedor.objects.get(identificacion=vendedor),
        )
        
        if Automovil.objects.filter(placa=placa).exists():
            messages.error(request, 'La placa '+placa+' ya está registrada')
            return redirect('listar_auto')
        auto.save()
        messages.success(request,'El automovil se registro correctamente')
        return redirect('listar_auto')
    return redirect('listar_auto')

def actualizar_auto(request, id):
    if request.method == 'POST':
        auto = Automovil.objects.get(id_auto=id)
        auto.modelo = request.POST.get('modelo')
        auto.marca = request.POST.get('marca').capitalize()
        auto.color = request.POST.get('color').capitalize()
        auto.precio = request.POST.get('precio')
        
        id_estado = request.POST.get('id_estado')
        id_categoria = request.POST.get('id_categoria')
        identificacion = request.POST.get('identificacion')

        estado = Estado.objects.get(id_estado=id_estado)
        categoria = Categoria.objects.get(id_categoria=id_categoria)
        vendedor = Vendedor.objects.get(identificacion=identificacion)

        auto.id_estado = estado
        auto.id_categoria = categoria
        auto.identificacion = vendedor
        
        nueva_placa = request.POST.get('placa')
        if Automovil.objects.exclude(id_auto=id).filter(placa=nueva_placa).exists():
            messages.error(request, 'La placa '+nueva_placa+' fue registrada anteriormente.')
        else:
            auto.placa = nueva_placa
            if 'imagen' in request.FILES:
                auto.imagen=request.FILES['imagen']     
            auto.save()
            messages.success(request, 'El automóvil se ha actualizado correctamente.')
            return redirect('listar_auto')
    else:
        auto = Automovil.objects.get(id_auto=id)
        return redirect('listar_auto',{'auto':auto})

def eliminar_auto(request,id):
    auto=Automovil.objects.get(id_auto=id)
    auto.delete()
    messages.success(request, 'Se elimino correctamente')
    return redirect('listar_auto')

def vehiculos(request):
    busqueda = request.GET.get("buscar")
    autos = Automovil.objects.all()
    range=request.GET.get("")
    if busqueda:
        autos = autos.filter(
            Q(marca__icontains=busqueda) |
            Q(modelo__icontains=busqueda) |
            Q(color__icontains=busqueda) |
            Q(id_estado__nombre__icontains=busqueda) |
            Q(id_categoria__nombre__icontains=busqueda)     
        ).distinct()
        if 'min_price' in request.GET and 'max_price' in request.GET:
            min_price = int(request.GET['min_price'])
            max_price = int(request.GET['max_price'])
            autos = Automovil.objects.filter(precio=(min_price,max_price))
        else:
            autos = Automovil.objects.all()
    data = {
        'autos': autos,
    }
    return render(request, 'paginas/vehiculo.html', data)

def administrador(request):
    return render(request,'paginas/administrador.html')

def categoria(request):
    if request.method == 'POST':
        nombre=request.POST.get('nombre').capitalize()

        categoria=Categoria(
            nombre=nombre
        )
        if Categoria.objects.filter(nombre=nombre).exists():
            messages.error(request,'Categoria fue registrada anteriormente')
            return render(request,'paginas/administrador.html')
        categoria.save()
        return render(request,'paginas/administrador.html')
    
def estado(request):
    if request.method == 'POST':
        nombre=request.POST.get('nombre').capitalize()

        estado=Estado(
            nombre=nombre
        )
        if Estado.objects.filter(nombre=nombre).exists():
            messages.error(request,'Estado fue registrada anteriormente')
            return render(request,'paginas/administrador.html')
        estado.save()
        return render(request,'paginas/administrador.html')
    
def rol(request):
    if request.method == 'POST':
        nombre=request.POST.get('nombre').capitalize()
        
        rol=Rol(
            nombre=nombre
        )
        if Rol.objects.filter(nombre=nombre).exists():
            messages.error(request,'Cargo fue registrada anteriormente')
            return render(request,'paginas/administrador.html')
        rol.save()
        roles=Rol.objects.all()
        data={
            'roles':roles
        }
        return render(request,'paginas/administrador.html',data)
    
