from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from .models import DBSession

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('view_page', '/{page}')
    config.add_route('edit_page', '/{page}/edit')
    config.add_route('add_page', '/add_page/{page}')
    config.include("pyramid_haml")
    config.scan()
    return config.make_wsgi_app()
