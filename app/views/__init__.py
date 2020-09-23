# Created by John Jiang at 2018/7/6 19:19

def init_views(app):
    from .files import files
    from .sms import sms
    # ...
    # Import more views here

    app.register_blueprint(files)
    app.register_blueprint(sms)
