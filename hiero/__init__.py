from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from .models import DBSession

def main(global_config, **settings):
    config = Configurator(settings=settings)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('get_pages',   '/pages') 
    config.add_route('get_page',    '/pages/{link_title}')
    config.add_route('edit_page',   '/pages/{link_title}/edit')
    config.add_route('add_page',    '/pages/{link_title}/add')
    config.add_route('remove_page', '/pages/{link_title}/remove')
    config.include("pyramid_haml")
    config.scan()
    return config.make_wsgi_app()
