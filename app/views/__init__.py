# Created by John Jiang at 2018/7/6 19:19


def init_views(app):
    from .update import update

    # ...
    # Import more views here

    app.register_blueprint(update)
