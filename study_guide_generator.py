from pathlib import Path
import subprocess
import sys
import textwrap

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.colors import HexColor
except Exception:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'reportlab'])
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.colors import HexColor


def wrap_text(text, width=95):
    return textwrap.wrap(text, width=width)


def add_title(pdf, text, y):
    pdf.setFillColor(HexColor('#1f2937'))
    pdf.setFont('Helvetica-Bold', 18)
    pdf.drawString(50, y, text)
    pdf.setStrokeColor(HexColor('#d1d5db'))
    pdf.line(50, y - 10, 540, y - 10)
    return y - 25


def add_section(pdf, title, y):
    pdf.setFillColor(HexColor('#0f172a'))
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(50, y, title)
    return y - 18


def add_paragraph(pdf, lines, y, font_size=10, indent=0):
    pdf.setFillColor(HexColor('#1f2937'))
    pdf.setFont('Helvetica', font_size)
    for line in lines:
        if y < 40:
            pdf.showPage()
            y = LETTER[1] - 50
        pdf.drawString(50 + indent, y, line)
        y -= font_size + 4
    return y


def create_pdf(output_path: Path):
    c = canvas.Canvas(str(output_path), pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    c.setFillColor(HexColor('#0f172a'))
    c.setFont('Helvetica-Bold', 24)
    c.drawString(50, y, 'Guía de estudio: Django + MySQL + CRUD Hotel')
    y -= 40

    c.setFillColor(HexColor('#475569'))
    c.setFont('Helvetica', 11)
    c.drawString(50, y, 'Proyecto de hotel con Django, CRUD completo y base de datos MySQL/MariaDB.')
    y -= 35

    sections = [
        (
            '1. Objetivo del proyecto',
            [
                'Crear una aplicación web en Django para gestionar habitaciones y reservas de un hotel.',
                'La app debe permitir crear, consultar, modificar y eliminar datos tanto desde la base de datos como desde la interfaz web.',
                'La base de datos usada puede ser MySQL/MariaDB o SQLite como respaldo, siendo MySQL el objetivo principal por la entrega.',
            ],
        ),
        (
            '2. Estructura del proyecto',
            [
                'App-Backend/',
                '  - manage.py',
                '  - hotel_project/settings.py',
                '  - hotel/models.py',
                '  - hotel/views.py',
                '  - hotel/urls.py',
                '  - hotel/forms.py',
                '  - templates/',
                '  - static/',
                '  - migrations/',
            ],
        ),
        (
            '3. Modelos principales',
            [
                'Habitacion: numero, tipo, precio_noche, capacidad, estado, descripcion, email_contacto, imagen_url.',
                'Reserva: habitacion, nombre, email, check_in, check_out.',
                'Los modelos tienen validaciones para que no se guarden datos inválidos.',
                'Ejemplo: precio_noche > 0, capacidad > 0, check_out > check_in.',
            ],
        ),
        (
            '4. CRUD en la base de datos',
            [
                'CREATE: Habitacion.objects.create(...) o Reserva.objects.create(...).',
                'READ: Habitacion.objects.all() o get(pk=...).',
                'UPDATE: objeto.precio_noche = ...; objeto.save().',
                'DELETE: objeto.delete().',
                'Esto demuestra que los datos realmente se crean, consultan, modifican y eliminan.',
            ],
        ),
        (
            '5. CRUD desde la web',
            [
                'Se usan vistas y formularios para crear, listar, editar y borrar registros desde el navegador.',
                'Rutas principales:',
                '  - /habitaciones/',
                '  - /habitaciones/crear/',
                '  - /habitaciones/<id>/editar/',
                '  - /habitaciones/<id>/eliminar/',
                '  - /reservas/',
                '  - /reservas/crear/',
                '  - /reservas/<id>/editar/',
                '  - /reservas/<id>/eliminar/',
            ],
        ),
        (
            '6. Formularios',
            [
                'HabitacionForm y ReservaForm en hotel/forms.py.',
                'Django usa ModelForm para crear los campos automáticamente desde los modelos.',
                'Los widgets agregan clases Bootstrap para una mejor presentación.',
                'Esto permite una interfaz más amigable y ordenada en la web.',
            ],
        ),
        (
            '7. Configuración de MySQL/MariaDB',
            [
                'Se define la base de datos en hotel_project/settings.py.',
                'Para usar MySQL se deben setear variables de entorno:',
                '  DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT.',
                'Ejemplo:',
                '  $env:DB_NAME="hotel_db"',
                '  $env:DB_USER="root"',
                '  $env:DB_PASSWORD=""',
                '  $env:DB_HOST="127.0.0.1"',
                '  $env:DB_PORT="3306"',
                'Si no existen esas variables, Django usa SQLite como respaldo.',
            ],
        ),
        (
            '8. Comandos clave de Django',
            [
                'Crear la base de datos en MySQL: CREATE DATABASE hotel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;',
                'Migrar: python manage.py migrate',
                'Crear superusuario: python manage.py createsuperuser',
                'Levantar servidor: python manage.py runserver',
                'Abrir shell: python manage.py shell',
                'Ejecutar pruebas: python manage.py test hotel',
            ],
        ),
        (
            '9. Comandos para arrancar la app',
            [
                'cd "C:\\Users\\Core i7 (13Gen)\\Desktop\\App-Backend-2\\App-Backend"',
                '$env:DB_NAME="hotel_db"',
                '$env:DB_USER="root"',
                '$env:DB_PASSWORD=""',
                '$env:DB_HOST="127.0.0.1"',
                '$env:DB_PORT="3306"',
                'python manage.py migrate',
                'python manage.py runserver',
                'Abrir esta URL: http://127.0.0.1:8000/',
            ],
        ),
        (
            '10. Ejemplo de operaciones CRUD en shell',
            [
                'from decimal import Decimal',
                'from hotel.models import Habitacion',
                '',
                '# CREATE',
                'h = Habitacion.objects.create(numero=101, tipo="Doble", precio_noche=Decimal("1200.00"), capacidad=2, estado="Disponible", email_contacto="recepcion@hotel.com")',
                '',
                '# READ',
                'print(Habitacion.objects.get(pk=h.pk))',
                '',
                '# UPDATE',
                'h.precio_noche = Decimal("1350.00")',
                'h.save()',
                '',
                '# DELETE',
                'h.delete()',
                'print(Habitacion.objects.filter(pk=h.pk).exists())',
            ],
        ),
        (
            '11. Requisitos que cumple el proyecto',
            [
                'Proyecto Django funcional.',
                'Aplicación Django creada.',
                'Modelos, vistas, URLs, templates y formularios.',
                'Base de datos MySQL/MariaDB configurada.',
                'Migraciones funcionando.',
                'CRUD completo en la web y en la base de datos.',
            ],
        ),
        (
            '12. Errores comunes y soluciones',
            [
                'Error de conexión MySQL: revisar usuario, contraseña, host y puerto.',
                'No se ven cambios: ejecutar python manage.py migrate.',
                'App no arranca: verificar que el entorno virtual está activo.',
                'Ruta incorrecta: usar la carpeta correcta del proyecto.',
                'Si la base de datos no existe, crearla antes con CREATE DATABASE ...',
            ],
        ),
        (
            '13. Resumen clave para memorizar',
            [
                'Django usa MVT: Modelo, Vista y Template.',
                'ModelForm ayuda a crear formularios desde los modelos.',
                'MySQL/MariaDB se conecta con variables de entorno y ENGINE django.db.backends.mysql.',
                'CRUD significa Create, Read, Update y Delete.',
                'La lógica real de negocio se define en models.py y views.py.',
                'La interfaz de usuario vive en templates/ y se gestiona con formularios.',
            ],
        ),
    ]

    for title, lines in sections:
        if y < 120:
            c.showPage()
            y = height - 50
        y = add_section(c, title, y)
        y = add_paragraph(c, lines, y, font_size=10)
        y -= 15

    c.save()


if __name__ == '__main__':
    desktop = Path.home() / 'Desktop'
    desktop.mkdir(exist_ok=True)
    output = desktop / 'Resumen_Django_Hotel.pdf'
    create_pdf(output)
    print(f'Archivo generado en: {output}')
