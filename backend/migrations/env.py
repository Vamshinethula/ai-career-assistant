from alembic import context
from app.database import Base, engine
from app import models

config = context.config


def migrate(connection):
    context.configure(connection=connection, target_metadata=Base.metadata,
                      render_as_batch=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    context.configure(url=engine.url,
                      target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
elif config.attributes.get('connection') is not None:
    migrate(config.attributes['connection'])
else:
    with engine.connect() as connection:
        migrate(connection)
