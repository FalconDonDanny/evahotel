# Guía de estudio completa: Django + MySQL + CRUD Hotel

## 1. ¿Qué es este proyecto?

Este proyecto es una aplicación web desarrollada con Django para gestionar habitaciones y reservas de un hotel.

La aplicación permite:
- Crear habitaciones
- Consultar habitaciones
- Editar habitaciones
- Eliminar habitaciones
- Crear reservas
- Consultar reservas
- Editar reservas
- Eliminar reservas

Esto cumple con el concepto de CRUD:
- C = Create
- R = Read
- U = Update
- D = Delete

---

## 2. Requisitos del proyecto

### Django
- Proyecto Django funcional
- Aplicación Django
- models.py
- views.py
- urls.py
- templates
- formularios

### Base de datos
- MySQL/MariaDB
- base de datos configurada
- tablas creadas
- migraciones funcionando

### Validaciones
- campos obligatorios
- tipos numéricos
- precios mayores que cero
- capacidad válida
- correos válidos
- fechas válidas

---

## 3. Estructura del proyecto

Proyecto principal:
- App-Backend/
  - manage.py
  - hotel_project/
    - settings.py
    - urls.py
    - wsgi.py
    - asgi.py
  - hotel/
    - __init__.py
    - models.py
    - views.py
    - urls.py
    - forms.py
    - tests.py
    - migrations/
  - templates/
    - base.html
    - hotel/
      - inicio.html
      - lista_habitaciones.html
      - detalle_habitacion.html
      - form_habitacion.html
      - form_reserva.html
      - lista_reservas.html
      - confirmar_eliminacion.html
  - static/
    - css/
      - styles.css

---

## 4. Modelos principales

### Habitacion
Atributos:
- numero
- tipo
- precio_noche
- capacidad
- estado
- descripcion
- email_contacto
- imagen_url
- created_at
- updated_at

### Reserva
Atributos:
- habitacion
- nombre
- email
- check_in
- check_out
- created_at

### Regla de negocio importante
Un modelo representa la estructura de la base de datos y la lógica de validación.

---

## 5. Validaciones que tiene el proyecto

### En Habitacion
- `numero` debe ser mayor que cero
- `capacidad` debe ser mayor que cero
- `precio_noche` debe ser mayor que cero
- `email_contacto` debe ser un correo válido
- `estado` debe ser parte de las opciones definidas

### En Reserva
- `check_out` debe ser posterior a `check_in`
- una habitación no puede tener reservas solapadas en fechas
- `email` debe ser válido
- `nombre` es obligatorio

### Implementación
Se usan:
- `EmailField`
- `DecimalField`
- `IntegerField`
- `DateField`
- `ForeignKey`
- `clean()`
- `save()` con `self.full_clean()`

Esto hace que Django valide los datos antes de guardar.

---

## 6. Formularios

Los formularios están en `hotel/forms.py`.

### HabitacionForm
Permite crear o editar una habitación desde la web.

### ReservaForm
Permite crear o editar una reserva desde la web.

### Uso
Los formularios se validan con:
```python
form.is_valid()
```

Si el formulario es válido, se guarda en la base de datos.

---

## 7. Vistas principales

En `hotel/views.py` hay vistas para:
- inicio
- lista de habitaciones
- detalle de habitación
- crear habitación
- editar habitación
- eliminar habitación
- crear reserva
- listar reservas
- editar reserva
- eliminar reserva

### Ejemplo de flujo
```python
def crear_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_habitaciones')
    else:
        form = HabitacionForm()
    return render(request, 'hotel/form_habitacion.html', {'form': form})
```

Esto cumple con el flujo CRUD.

---

## 8. URLs del proyecto

En `hotel/urls.py` se definen rutas como:
- '' -> inicio
- 'habitaciones/' -> lista
- 'habitaciones/crear/' -> crear
- 'habitaciones/<int:pk>/' -> detalle
- 'habitaciones/<int:pk>/editar/' -> editar
- 'habitaciones/<int:pk>/eliminar/' -> eliminar
- 'reservas/' -> listar reservas
- 'reservas/crear/' -> crear reserva
- 'reservas/<int:pk>/editar/' -> editar reserva
- 'reservas/<int:pk>/eliminar/' -> eliminar reserva

En `hotel_project/urls.py` se incluye la app principal:
```python
path('', include('hotel.urls'))
```

---

## 9. CRUD completo a nivel web

### Crear
Desde el navegador se llena un formulario y se guarda el dato.

### Consultar
Se muestra la lista de habitaciones o reservas.

### Modificar
Se abre el formulario con los datos actuales y se actualiza.

### Eliminar
Se confirma la eliminación antes de borrar el registro.

Esto permite que el usuario final realice todo el CRUD desde la aplicación web.

---

## 10. CRUD completo a nivel base de datos

También se puede trabajar directamente desde el shell de Django o desde MySQL.

### Ejemplo de create
```python
from decimal import Decimal
from hotel.models import Habitacion

Habitacion.objects.create(
    numero=101,
    tipo='Doble',
    precio_noche=Decimal('1200.00'),
    capacidad=2,
    estado='Disponible',
    email_contacto='recepcion@hotel.com'
)
```

### Read
```python
Habitacion.objects.all()
Habitacion.objects.get(pk=1)
```

### Update
```python
h = Habitacion.objects.get(pk=1)
h.precio_noche = Decimal('1500.00')
h.save()
```

### Delete
```python
h.delete()
```

---

## 11. Configuración de MySQL/MariaDB

En `hotel_project/settings.py` se configuró un soporte para MySQL/MariaDB con variables de entorno.

### Variables necesarias
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT

### Ejemplo
```powershell
$env:DB_NAME="hotel_db"
$env:DB_USER="root"
$env:DB_PASSWORD=""
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"
```

### Base de datos
```sql
CREATE DATABASE hotel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Si no hay variables
El proyecto usa SQLite como respaldo.

---

## 12. Migraciones

Las migraciones permiten crear las tablas en la base de datos.

### Comando
```powershell
python manage.py migrate
```

### Resultado esperado
Django crea las tablas de:
- admin
- auth
- sessions
- contenttypes
- hotel

---

## 13. Cómo arrancar la app

### En PowerShell
```powershell
cd "C:\Users\Core i7 (13Gen)\Desktop\App-Backend-2\App-Backend"

$env:DB_NAME="hotel_db"
$env:DB_USER="root"
$env:DB_PASSWORD=""
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="3306"

python manage.py migrate
python manage.py runserver
```

### Abrir en navegador
```text
http://127.0.0.1:8000/
```

---

## 14. Verificación con pruebas

Se ejecutaron pruebas en Django con:
```powershell
python manage.py test hotel
```

Resultado verificado:
- 8 pruebas ejecutadas
- todas OK

Esto demuestra que el proyecto funciona correctamente.

---

## 15. Resumen para memorizar

### Concepto principal
Django trabaja con el patrón MVT:
- Modelo = datos y validaciones
- Vista = lógica y control
- Template = interfaz HTML

### Relación con el CRUD
- Crear = formulario + post + save
- Consultar = querysets + render
- Editar = formulario + instance + save
- Eliminar = borrar objeto + redirect

### Relación con MySQL
- la base de datos se configura en settings.py
- se crean tablas con migraciones
- los datos quedan persistidos en la base de datos

### Importancia de las validaciones
Evitan guardar datos incorrectos como:
- precio negativo
- capacidad cero
- correo inválido
- fechas incorrectas

---

## 16. Frases clave para recordar en una presentación

> Este proyecto implementa CRUD completo en Django utilizando modelos, formularios y vistas. La aplicación permite gestionar habitaciones y reservas desde la interfaz web y también desde la propia base de datos.

> Las validaciones se realizan tanto en los modelos como en los formularios para asegurar que los datos sean correctos antes de guardarlos.

> MySQL/MariaDB se configura con variables de entorno y permite persistir los datos de manera segura y ordenada.

---

## 17. Recomendaciones finales

1. Estudia `models.py` primero.
2. Después `views.py` y `urls.py`.
3. Luego `forms.py`.
4. Finalmente `templates/`.
5. Practica el flujo CRUD completo varias veces.
6. Repite los comandos de terminal y migración.
7. Haz pruebas con datos reales.

---

## 18. Conclusión

Este proyecto cumple con la mayoría de los requisitos de un proyecto Django profesional:
- aplicación web funcional
- CRUD completo
- base de datos configurada
- validaciones de datos
- modelo y formularios bien implementados
- migraciones configuradas
- MySQL/MariaDB compatible

Si repases esta guía y practicas cada sección, podrás entender y explicar el proyecto con claridad.
