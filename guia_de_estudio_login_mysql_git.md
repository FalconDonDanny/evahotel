# Guía de estudio: Hotel Vista del Mar (Django + MySQL + Git)

## 1. Arquitectura (MTV)

| Capa | Qué es | Archivo(s) |
|---|---|---|
| Model | Tablas y reglas de negocio | `hotel/models.py` |
| Template | HTML que ve el usuario | `templates/base.html`, `templates/hotel/*`, `templates/registration/*` |
| View | Lógica de cada petición | `hotel/views.py` |
| URLs | Enruta una URL a una vista | `hotel_project/urls.py`, `hotel/urls.py` |
| Forms | Validan y guardan datos | `hotel/forms.py` |
| Settings | Configuración (BD, apps, login) | `hotel_project/settings.py` |

Flujo: navegador -> `urls.py` -> vista -> formulario/modelo -> plantilla -> respuesta.

Estructura: proyecto `hotel_project`, app `hotel`, carpeta `App-Backend/` con `manage.py`.

## 2. Modelos (`hotel/models.py`)

**Habitacion**: `numero` (IntegerField, unique), `tipo` (CharField), `precio_noche` (DecimalField), `capacidad` (IntegerField), `estado` (choices: Disponible, Ocupada, Mantenimiento, Reservada), `descripcion` (TextField), `email_contacto` (EmailField opcional, conservado por compatibilidad), `imagen_url` (URLField), `created_at` / `updated_at`.
Tabla en MySQL: `hotel_habitacion`.

**Reserva**: `habitacion` (ForeignKey a Habitacion, `related_name='reservas'`, `on_delete=CASCADE`), `nombre`, `email`, `check_in`, `check_out`, `created_at`.
Tabla en MySQL: `hotel_reserva`.

- Clave primaria: `id` automática (`DEFAULT_AUTO_FIELD = BigAutoField`).
- Relación: una Habitación tiene muchas Reservas (1 a N).
- `clean()` contiene las reglas de negocio; `save()` llama a `full_clean()` para que ningún dato inválido se guarde, ni desde el shell.

## 3. Validaciones

Reglas en el modelo (`clean()`):
- Habitación: número > 0, capacidad entre 1 y 20, precio > 0, tipo no vacío.
- Reserva: salida posterior a entrada; entrada no en el pasado (al crear); habitación en Mantenimiento no se reserva; no se solapa con otra reserva de la misma habitación.

Reglas en formularios (`hotel/forms.py`):
- `ReservaForm.clean_nombre`: mínimo 3 caracteres, limpia espacios.
- `RegistroForm.clean_email`: correo único (sin distinguir mayúsculas).
- `PagoForm.clean_numero_tarjeta`: solo dígitos, empieza con 4 (Visa), algoritmo de Luhn.
- `PagoForm.clean_vencimiento`: formato MM/AA y no vencida.

Diferencia clave: `clean()` del modelo valida el objeto completo; `clean_<campo>()` del formulario valida un solo campo. Los errores se muestran junto a cada campo en las plantillas.

## 4. Autenticación

- App `django.contrib.auth` (modelo `User`, tabla `auth_user`).
- Vistas: `LoginView` y `LogoutView` (de `django.contrib.auth.views`) y la vista propia `registro`.
- URLs: `/login/` (name `login`), `/logout/` (name `logout`), `/registro/` (name `registro`) en `hotel_project/urls.py`.
- Formularios: `LoginForm` (hereda `AuthenticationForm`) y `RegistroForm` (hereda `UserCreationForm`, añade `email`).
- Registro sencillo: pide correo y contraseña dos veces; el nombre de usuario se genera automáticamente desde el correo. Se puede iniciar sesión usando el correo.
- Contraseña de registro: se permiten claves cortas y numéricas; el campo y su confirmación son obligatorios.
- Agregar habitaciones es público y no solicita correo ni contraseña. Editar y eliminar habitaciones siguen requiriendo iniciar sesión.
- Settings: `LOGIN_URL='login'`, `LOGIN_REDIRECT_URL='inicio'`, `LOGOUT_REDIRECT_URL='inicio'`.
- Protección: decorador `@login_required` en crear/editar/eliminar habitación, crear/editar/eliminar/listar reservas y pago. Si no hay sesión redirige a `/login/?next=...`.
- Logout por POST con `{% csrf_token %}` (más seguro que GET).
- Contraseñas: se guardan con hash; hay validadores en `AUTH_PASSWORD_VALIDATORS`.
- Plantillas: `registration/login.html`, `registration/registro.html`; el menú de `base.html` cambia según `user.is_authenticated`.
- Públicas: inicio, lista y detalle de habitaciones, disponibilidad, login y registro.

## 5. Vistas y URLs (`hotel/views.py`, `hotel/urls.py`)

| Nombre de URL | Ruta | Vista |
|---|---|---|
| `inicio` | `/` | `inicio` |
| `pago` | `/pago/` | `pago` |
| `lista_habitaciones` | `/habitaciones/` | `lista_habitaciones` |
| `disponibilidad` | `/disponibilidad/` | `disponibilidad` |
| `crear_habitacion` | `/habitaciones/crear/` | `crear_habitacion` |
| `detalle_habitacion` | `/habitaciones/<pk>/` | `detalle_habitacion` |
| `editar_habitacion` | `/habitaciones/<pk>/editar/` | `editar_habitacion` |
| `eliminar_habitacion` | `/habitaciones/<pk>/eliminar/` | `eliminar_habitacion` |
| `listar_reservas` | `/reservas/` | `listar_reservas` |
| `crear_reserva` | `/reservas/crear/` | `crear_reserva` |
| `editar_reserva` | `/reservas/<pk>/editar/` | `editar_reserva` |
| `eliminar_reserva` | `/reservas/<pk>/eliminar/` | `eliminar_reserva` |

CRUD = Create (crear), Read (lista/detalle), Update (editar), Delete (eliminar).
Patrón de las vistas de formulario: si es POST y el formulario es válido -> `form.save()`, mensaje y `redirect`; si no, vuelve a mostrar el formulario con errores.

Disponibilidad: `disponibilidad` recibe `check_in` y `check_out` por GET, excluye habitaciones en Mantenimiento y las que tienen reservas solapadas (`reservas__check_in__lt=check_out, reservas__check_out__gt=check_in`).

## 6. MySQL y migraciones

- Driver: PyMySQL, con `pymysql.install_as_MySQLdb()` en `settings.py` (Django busca `MySQLdb`).
- Variables de entorno: `DB_ENGINE` (por defecto `mysql`), `DB_NAME` (`hotel_db`), `DB_USER` (`root`), `DB_PASSWORD`, `DB_HOST` (`127.0.0.1`), `DB_PORT` (`3306`). Con `DB_ENGINE=sqlite` usa SQLite (solo pruebas).
- Servidor usado: MySQL de XAMPP (MariaDB 10.4.32).
- Problema: Django 6.1 exige MariaDB 10.11 o superior. Solución: backend propio `hotel_project/db_backend/base.py` que omite el chequeo de versión y desactiva `INSERT ... RETURNING` (MariaDB 10.5+). `settings.py` lo usa como `ENGINE`.
- Comandos:
  - `python manage.py makemigrations`: genera archivos de migración a partir de los modelos.
  - `python manage.py migrate`: aplica las migraciones a la base de datos.
  - `SHOW TABLES;` en MySQL: verifica las tablas.
- Migraciones del proyecto: `0001_initial`, `0002_habitacion_imagen_url`, `0003_reserva`.
- Crear la base: `CREATE DATABASE hotel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
- Persistencia: los formularios de habitación, reserva y registro guardan en MySQL. El formulario de pago es demostrativo y no guarda nada (no se almacenan tarjetas).

## 7. Interfaz

- Plantilla base `templates/base.html`; las demás usan `{% extends 'base.html' %}` y `{% block content %}`.
- Bootstrap 5 (CDN), CSS propio en `static/css/styles.css`, tema claro/oscuro con `localStorage`.
- Responsive: `meta viewport`, grid de Bootstrap (`row`, `col-*`), menú colapsable (`navbar-expand-lg`).
- Mensajes: framework `django.contrib.messages`, mostrados como alertas Bootstrap.
- Seguridad en formularios: `{% csrf_token %}` en todos los POST.

## 8. Pruebas (`hotel/tests.py`)

22 pruebas con `TestCase` (Django usa una base temporal `test_hotel_db`): modelos, solapamiento, configuración MySQL, rutas, autenticación (redirección, registro con correo, correo duplicado, login por correo y logout) y validaciones (pasado, mantenimiento, Luhn, vencimiento).
Comando: `python manage.py test`.

## 9. Git

Ramas por funcionalidad (todas fusionadas a `main` con `git merge --no-ff`):

| Rama | Contenido |
|---|---|
| `feature/login` | Login, registro, logout, `@login_required` |
| `feature/validaciones` | Reglas en modelos y formularios |
| `feature/mysql-ui` | MySQL por defecto, `requirements.txt`, `.env.example`, mensajes |
| `feature/pruebas` | Pruebas automáticas |

Ramas por integrante (genéricas): `integrante1-login`, `integrante2-validaciones`, `integrante3-mysql-ui`, `integrante4-pruebas`.
Conflicto practicado: `integrante1-footer` e `integrante2-footer` modificaron la misma línea de `base.html`; se resolvió conservando ambos cambios.

Comandos útiles: `git init`, `git branch`, `git checkout -b <rama>`, `git add`, `git commit -m`, `git merge --no-ff`, `git log --oneline --graph`, `git remote add origin <url>`, `git push -u origin <rama>`.
Conflicto: Git marca `<<<<<<<`, `=======` y `>>>>>>>`; se edita el archivo, se hace `git add` y `git commit`.
`.gitignore` excluye `.venv/`, `__pycache__/`, `db.sqlite3`, `.env` y `staticfiles/`.

## 10. Preguntas probables y respuestas cortas

1. ¿Qué es MTV? Model (datos), Template (HTML) y View (lógica); es la versión de Django del patrón MVC.
2. ¿Qué hace `@login_required`? Redirige a `LOGIN_URL` si el usuario no tiene sesión.
3. ¿Por qué el logout es POST? Evita que un enlace externo cierre la sesión (CSRF).
4. ¿Diferencia entre `makemigrations` y `migrate`? El primero crea los archivos de migración, el segundo los aplica a la base.
5. ¿Por qué `pymysql.install_as_MySQLdb()`? Django espera el módulo `MySQLdb`; PyMySQL lo sustituye.
6. ¿Qué es una `ForeignKey`? Relación N a 1; `Reserva.habitacion` apunta a `Habitacion`.
7. ¿Qué es `related_name='reservas'`? Permite `habitacion.reservas.all()`.
8. ¿Por qué `save()` llama a `full_clean()`? Para validar siempre, no solo en formularios.
9. ¿Qué evita `{% csrf_token %}`? Ataques Cross-Site Request Forgery.
10. ¿Cómo se detecta el solapamiento de reservas? `check_in < otra.check_out` y `check_out > otra.check_in`.
11. ¿Qué es el algoritmo de Luhn? Suma de verificación para validar números de tarjeta.
12. ¿Cómo se resuelve un conflicto de merge? Editar el archivo, quitar los marcadores, `git add` y `git commit`.
13. ¿Por qué un backend propio de base de datos? XAMPP trae MariaDB 10.4 y Django 6.1 pide 10.11 o superior.
14. ¿Qué diferencia hay entre `clean()` y `clean_<campo>()`? El primero valida el objeto completo; el segundo un campo del formulario.
15. ¿Por qué el pago no guarda tarjetas? Es demostrativo; guardar datos de tarjeta es un riesgo de seguridad.

## 11. Comandos para la demostración

```powershell
# MySQL de XAMPP activo (panel de XAMPP) y desde App-Backend:
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py runserver 8000
..\.venv\Scripts\python.exe manage.py test
git log --oneline --graph
```
Flujo a mostrar: registrarse, iniciar sesión, crear habitación, consultar disponibilidad, reservar, intentar una reserva solapada (error), cerrar sesión, abrir una URL protegida (redirige a login) y `SHOW TABLES;` / `SELECT * FROM hotel_reserva;` en MySQL.
