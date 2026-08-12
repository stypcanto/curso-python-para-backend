from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Nuestros modelos: hace falta importar los 3 (mismo motivo que en
# main.py) para que Base.metadata sepa que existen las 3 tablas.
from core.config import settings
from db.database import Base
from models.user import User
from models.category import Category
from models.ticket import Ticket

# Este es el objeto de configuración de Alembic — da acceso a los
# valores del archivo alembic.ini que se está usando.
config = context.config

# Usa la misma DATABASE_URL del .env (core/config.py) en vez de la que
# viene hardcodeada en alembic.ini — una sola fuente de verdad. Así no
# hay que mantener la URL de conexión escrita en dos lugares distintos.
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpreta el archivo de configuración para el logging de Python.
# Esta línea deja armados los loggers (root, sqlalchemy, alembic).
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── target_metadata: el corazón de "autogenerate" ──────────────────
#
# target_metadata = Base.metadata
#
# Base.metadata es un objeto MetaData de SQLAlchemy — un catálogo que
# se va llenando solo, a medida que cada class Modelo(Base) se
# ejecuta (User, Category, Ticket). Ahí queda registrado el nombre de
# cada tabla, sus columnas, tipos y FK.
#
# Al asignarlo acá como target_metadata, le decimos a Alembic:
# "esto es lo que el esquema DEBERÍA ser". Cuando corrés
# `alembic revision --autogenerate`, Alembic compara ese "debería
# ser" (target_metadata) contra lo que la base de datos REALMENTE
# tiene en este momento, y genera automáticamente el script de
# migración con la diferencia (crear una tabla, agregar una columna,
# etc.) — sin este import, Alembic no tendría con qué comparar y
# `--autogenerate` no generaría nada.
target_metadata = Base.metadata

# Otros valores de configuración, si hicieran falta, se leerían así:
# mi_opcion = config.get_main_option("mi_opcion")


def run_migrations_offline() -> None:
    """Corre las migraciones en modo 'offline'.

    Acá se configura el contexto solo con una URL (sin abrir una
    conexión/Engine real) — sirve para generar el SQL de la migración
    como texto, sin necesitar el driver de la base de datos instalado.
    Las llamadas a context.execute() imprimen el SQL generado en vez
    de ejecutarlo contra la base.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Corre las migraciones en modo 'online' (el que usamos acá).

    Este es el modo real: abre una conexión (Engine) de verdad contra
    Postgres y aplica la migración en una transacción.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Alembic decide solo qué modo usar según cómo se lo invoque
# (`alembic upgrade head` corre siempre en modo online).
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
