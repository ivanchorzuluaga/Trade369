# Trade360 (Django)

Proyecto Django para gestion de usuarios, contratos, valores e intereses.

## Stack
- Python 3.8+
- Django 4.0.6
- PostgreSQL (por defecto)
- SQLAlchemy, pandas, numpy, python-dateutil

## Requisitos
- Python 3.8+ instalado
- PostgreSQL local (si usas la configuracion por defecto)

## Instalacion
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install Django==4.0.6 psycopg2-binary pandas numpy python-dateutil SQLAlchemy
```

## Configuracion de base de datos
Por defecto el proyecto apunta a PostgreSQL en `Trade2`.

Archivo: `/Users/ivanzuluaga/Documents/Trabajo_Code/TRADE369/Trade360/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Trade2',
        'USER': 'postgres',
        'PASSWORD': '<TU_PASSWORD>',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

**Importante:** en `/Users/ivanzuluaga/Documents/Trabajo_Code/TRADE369/user/views.py` hay un engine de SQLAlchemy con credenciales propias. Asegura que el password coincida con tu base local.

### Opcion SQLite (rapida para pruebas)
Puedes reactivar SQLite comentado en `settings.py`, pero ten en cuenta que el dashboard usa SQLAlchemy contra PostgreSQL. Si cambias a SQLite, deberas ajustar esa parte.

## Migraciones y superusuario
```bash
python manage.py migrate
python manage.py createsuperuser
```

## Correr en local
```bash
python manage.py runserver
```

## Dump de base de datos (opcional)
Hay un dump en `/Users/ivanzuluaga/Documents/Trabajo_Code/TRADE369/17-05-2023.sql`. Es un `pg_dump` en formato custom, se restaura con `pg_restore`.

Ejemplo:
```bash
pg_restore -U postgres -d Trade2 /Users/ivanzuluaga/Documents/Trabajo_Code/TRADE369/17-05-2023.sql
```

## Notas
- Hay credenciales sensibles en `settings.py`. Para produccion, mover a variables de entorno.
- Email usa SMTP de Gmail. Para desarrollo puedes cambiar a `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`.
