from django.shortcuts import render
from .models import Categoria, Mascota, Galeria

# importar el modelo de la tabla User
from django.contrib.auth.models import User
# importar librerias para validar el login
from django.contrib.auth import authenticate,logout,login as login_aut
# importar libreria de decorador que permite evitar el ingreso a paginas 
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.
def crear_usuario(request):
    if request.POST:
        nombre = request.POST.get("txtNombre")
        apellido = request.POST.get("txtApellido")
        email= request.POST.get("txtEmail")
        nom_usuario= request.POST.get("txtUsuario")
        pass1= request.POST.get("txtPass1")
        pass2= request.POST.get("txtPass2")

        if pass1!=pass2:
            contexto={"mensaje":"password no son iguales"}
            return render(request,"crear_usuario.html",contexto)

        try:
            usu = User.objects.get(username=nom_usuario)
            contexto={"mensaje","usuario ya existe"}
            return render(request,"crear_usuario.html",contexto)
        except:
            usu = User()
            usu.first_name= nombre
            usu.last_name= apellido
            usu.email= email
            usu.username= nom_usuario
            usu.set_password(pass1)
            usu.save()

            us = authenticate(request,username=nom_usuario,password=pass1)
            login_aut(request,us)

            return render(request,"index.html")


    return render(request,"crear_usuario.html")

def cerrar_sesion(request):
    logout(request)
    return render(request,"index.html")

def login(request):
    if request.POST:
        nombre = request.POST.get("txtNombre")
        contra = request.POST.get("txtPass")
        us = authenticate(request,username=nombre,password=contra)
        if us is not None and us.is_active:
            login_aut(request,us)
            return render(request,"index.html")
        else:
            contexto= {"mensaje":"usuario o contraseña incorrecto"}
            return render(request,"login.html",contexto)
    return render(request, "login.html")

def inicio(request):
    mascotas = Mascota.objects.filter(publicar=True).order_by('-nombre')[:3]
    contexto = {"mascotas":mascotas}
    categorias = Categoria.objects.all()
    contexto["categorias"] = categorias
    return render(request, "index.html",contexto)

def galeria(request):
    mascotas = Mascota.objects.filter(publicar=True)
    categorias = Categoria.objects.all()
    contexto= {"mascotas": mascotas,"categorias":categorias}
    return render(request, "galeria2.html",contexto)

def filtrar_categoria(request):
    mascotas = Mascota.objects.filter(publicar=True)
    categorias = Categoria.objects.all()
    cant= Mascota.objects.filter(publicar=True).count()
    if request.POST:
        cate = request.POST.get("cboCategoria")
        obj_categoria = Categoria.objects.get(nombre=cate)
        mascotas = Mascota.objects.filter(categoria=obj_categoria).filter(publicar=True)
        cant = Mascota.objects.filter(categoria=obj_categoria).filter(publicar=True).count()
    contexto= {"mascotas": mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria2.html",contexto)

def filtrar_cate(request,id):
    categorias = Categoria.objects.all()
    
    obj_categoria = Categoria.objects.get(nombre=id)
    mascotas = Mascota.objects.filter(categoria=obj_categoria).filter(publicar=True)
    cant = Mascota.objects.filter(categoria=obj_categoria).filter(publicar=True).count()
    
    contexto= {"mascotas": mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria2.html",contexto)

def filtrar_descripcion(request):
    mascotas = Mascota.objects.filter(publicar=True)
    cant = Mascota.objects.filter(publicar=True).count()
    categorias = Categoria.objects.all()
    if request.POST:
        desc = request.POST.get("txtDescripcion")
        mascotas = Mascota.objects.filter(descripcion__contains=desc).filter(publicar=True)
        cant = Mascota.objects.filter(descripcion__contains=desc).filter(publicar=True).count()
    contexto= {"mascotas": mascotas,"categorias":categorias,"cantidad":cant}
    return render(request, "galeria2.html",contexto)

def buscar_nombre(request):
    mensaje=""
    if request.POST:
        nombre = request.POST.get("txtMascota")
        try:
            masc = Mascota.objects.get(nombre=nombre)
            galeria = Galeria.objects.filter(mascota=masc)
            contexto = {"mascota":masc,"galeria":galeria}
            return render(request, "ficha.html", contexto)
        except:
            mensaje="No encontro mascota "+nombre

    mascotas = Mascota.objects.filter(publicar=True).order_by('-nombre')[:3]
    contexto = {"mascotas":mascotas}
    categorias = Categoria.objects.all()
    contexto["categorias"] = categorias
    contexto["mensaje"] = mensaje
    return render(request, "index.html",contexto)
    
def formulario(request):
    return render(request, "formulario.html")

def ficha_mascota(request, id):
    masc = Mascota.objects.get(nombre=id)
    galeria = Galeria.objects.filter(mascota=masc)
    contexto = {"mascota":masc,"galeria":galeria}
    return render(request, "ficha.html", contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.add_mascota',login_url='/login/')
def registro(request):
    nom_user= request.user.username # recuperar el nombre del usuario autentificado
    mensaje=""   
    if request.POST:
        nombre = request.POST.get("txtNombre")
        edad = request.POST.get("txtEdad")
        desc = request.POST.get("txtDesc")
        cate = request.POST.get("cboCategoria")
        imagen = request.FILES.get("txtImg")
        obj_cate = Categoria.objects.get(nombre=cate) # select * from Categoria where nombre=''
        
        try:
            mas = Mascota.objects.get(nombre=nombre)
            mensaje ="Mascota Existe"
        except:
            mas = Mascota()
            mas.nombre = nombre
            mas.edad = edad
            mas.descripcion = desc
            mas.categoria = obj_cate
            mas.usuario = nom_user

            if imagen is not None:
                mas.imagen = imagen
            
            mas.save()
            mensaje="grabo"

    categorias = Categoria.objects.all() # select * from Categoria
    mascotas = Mascota.objects.filter(usuario=nom_user)
    contexto = {"mensaje":mensaje,"categorias":categorias,"mascotas":mascotas}
    cant = Mascota.objects.filter(usuario=nom_user).count()
    contexto["cantidad"]=cant
    return render(request, "registro.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.delete_mascota',login_url='/login/')
def eliminar(request,id):
    try:
        mas = Mascota.objects.get(nombre=id)
        mas.delete()
        mensaje="elimino"
    except:
        mensaje="no elimino"
    
    categorias = Categoria.objects.all() # select * from Categoria
    mascotas = Mascota.objects.all()

    contexto = {"mensaje":mensaje,"categorias":categorias,"mascotas":mascotas}
    return render(request, "registro.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.view_mascota',login_url='/login/')
def buscar_modificar(request,id):
    try:
        mas = Mascota.objects.get(nombre=id)
        categorias = Categoria.objects.all() # select * from Categoria
        contexto = {"categorias":categorias,"mascota":mas}
        return render(request, "modificar.html",contexto)

    except:
        mensaje="no encontro mascota"
    
    categorias = Categoria.objects.all() # select * from Categoria
    mascotas = Mascota.objects.all()

    contexto = {"mensaje":mensaje,"categorias":categorias,"mascotas":mascotas}
    return render(request, "registro.html",contexto)

@login_required(login_url='/login/')
@permission_required('misPerris.change_mascota',login_url='/login/')
def modificar(request):
    nom_user = request.user.username
    if request.POST:
        nombre = request.POST.get("txtNombre")
        edad = request.POST.get("txtEdad")
        desc = request.POST.get("txtDesc")
        cate = request.POST.get("cboCategoria")
        imagen = request.FILES.get("txtImg")
        obj_cate = Categoria.objects.get(nombre=cate) # select * from Categoria where nombre=''
        
        try:
            mas = Mascota.objects.get(nombre=nombre)
            mas.edad=edad
            mas.descripcion=desc
            mas.categoria= obj_cate

            if imagen is not None:
                mas.imagen=imagen

            mas.comentario='--'
            mas.save()
            mensaje="modifico mascota "+nombre
        except:
            mensaje="no modifico"

    categorias = Categoria.objects.all() # select * from Categoria
    mascotas = Mascota.objects.filter(usuario=nom_user)
    contexto = {"mensaje":mensaje,"categorias":categorias,"mascotas":mascotas}
    contexto["cantidad"] = Mascota.objects.filter(usuario=nom_user).count()
    return render(request, "registro.html",contexto)

def adoptar(request,id):
    mensaje=""
    try:
        mas = Mascota.objects.filter(publicar=True).get(nombre=id)
        mas.dueno = request.user.username
        mas.publicar = False
        mas.save()
        mensaje="Adoptada"
    except:
        mensaje="No Pudo Adoptar Mascota"

    masc = Mascota.objects.get(nombre=id)
    contexto = {"mascota":masc,"mensaje":mensaje}
    return render(request, "ficha.html", contexto)

def admin_usuario(request):
    mascotas = Mascota.objects.filter(dueno = request.user.username)
    contexto = {"mascotas":mascotas}
    return render(request,"admin_usuario.html",contexto)

def devolver(request,id):
    mensaje=""
    try:
        mas = Mascota.objects.filter(publicar=False).get(nombre=id)
        mas.dueno = '--'
        mas.save()
        mensaje = "Mascota devuelta"
    except:
        mensaje="No Pudo Devolver la Mascota"

    mascotas = Mascota.objects.filter(dueno = request.user.username)
    contexto = {"mascotas":mascotas,"mensaje":mensaje}
    return render(request,"admin_usuario.html",contexto)
    
def insertar_galeria(request):
    mensaje=""
    if request.POST:
        nom_mascota = request.POST.get("txtMascota")
        imagen = request.FILES.get("txtImg")
        obj_mascota = Mascota.objects.get(nombre=nom_mascota)
        gale = Galeria()
        gale.imagen = imagen
        gale.mascota = obj_mascota
        gale.save()
        mensaje = "Agrego imagen a mascota "+nom_mascota

    nom_user = request.user.username    
    categorias = Categoria.objects.all() # select * from Categoria
    mascotas = Mascota.objects.filter(usuario=nom_user)
    contexto = {"mensaje":mensaje,"categorias":categorias,"mascotas":mascotas}
    cant = Mascota.objects.filter(usuario=nom_user).count()
    contexto["cantidad"]=cant
    return render(request, "registro.html",contexto)    

