# Created by John Jiang at 2018/7/6 13:50

from flask import Config, Flask, Response, json, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix

from . import extensions, logging, models, views


class MyFlask(Flask):
    # 改进默认的 config 对象，可以使用 dot 访问配置
    # 错误的实现会导致 flask-admin bootstarp3/admin/lib.html 中 config.MAPBOX_MAP_ID 访问出错
    class config_class(Config):
        def __getattr__(self, item):
            try:
                return self.__getitem__(item)
            except KeyError:
                return super().__getattr__(item)

    # 改进默认的 json encoder，可以编码 set、datetime 等类型
    class json_encoder(json.JSONEncoder):
        def default(self, o):
            return super().default(o)

    # 改进默认的 response 类型，可以从 view funciton 中直接返回 dict
    class response_class(Response):
        # 不加 classmethod 会出错
        @classmethod
        def force_type(cls, response, environ=None):
            if isinstance(response, dict):
                response = jsonify(response)
            return super().force_type(response, environ)


# create_app 是整个项目的入口
def create_app(config_name):
    app = MyFlask(
        __name__,
        static_folder=None,
        instance_relative_config=True
    )
    app.config.from_object('config.{}.Config'.format(config_name))

    logging.init_loggers(app)
    models.init_models(app)
    extensions.init_extentions(app)
    views.init_views(app)

    @app.shell_context_processor
    def make_context():
        return dict(app=app)

    app.logger.info('App created')

    # Apply some middlewares
    # If you deploy your application using one of these servers
    # behind an HTTP proxy you will need this.
    app.wsgi_app = ProxyFix(app, x_proto=1, x_for=1)
    return app
