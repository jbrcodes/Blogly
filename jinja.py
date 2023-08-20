from datetime import datetime



def init_app(app):
    app.jinja_env.filters['format_datetime'] = format_datetime


def format_datetime(dt):
    fmt = '%d %b %Y @ %H:%M:%S'

    return dt.strftime(fmt)