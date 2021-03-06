import logging

import bottle
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from truckpad.bottle.cors import CorsPlugin

logger= logging.getLogger(__name__)

Base = declarative_base()
engine = create_engine('sqlite:///db', echo=True)
app = bottle.Bottle()
plugin = sqlalchemy.Plugin(
    engine,  # SQLAlchemy engine created with create_engine function.
    Base.metadata,  # SQLAlchemy metadata, required only if create=True.
    keyword='db',  # Keyword used to inject session database in a route (default 'db').
    create=True,  # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True,  # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False
    # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)
app.install(plugin)
app.mount('/api', app)
app.config.load_config('config.ini')

import fibi.routes

logger.warning("CORS ENABLED!")
app.install(CorsPlugin(origins=['*']))
