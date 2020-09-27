# Created by John Jiang at 2018/9/27 11:22
import click
from flask_migrate import Migrate


def init_migrate(app):
    # flask-migrate setup.py 中定义了 flask.commands 的 entry_points
    # entry_points={
    #         'flask.commands': [
    #             'db=flask_migrate.cli:db'
    #         ],
    #     },
    # FlaskGroup 能够自动找到并注册 flask-migrate.cli 中定义的命令
    # 所以可以直接使用 flask db init 等命令
    from app.models import db

    migrate = Migrate(db=db, compare_type=True, compare_server_default=True)
    migrate.init_app(app)


# 在这里添加自定义的 flask 子命令
def init_cli(app):
    init_migrate(app)

    # app.cli 是一个 AppGroup 实例
    @app.cli.command("profile", short_help="Profile application")
    @click.option(
        "-h",
        "--host",
        default="localhost",
        envvar="FLASK_RUN_HOST",
        help="The host for the application",
    )
    @click.option("-p", "--port", default=5000, help="The port for the server")
    def profile_command(host, port):
        from werkzeug.middleware.profiler import ProfilerMiddleware
        from werkzeug.serving import run_simple

        wrapped_app = ProfilerMiddleware(app)
        run_simple(host, port, wrapped_app)

    @app.cli.command("compile-proto", short_help="Compoile Protobuf")
    def compile_protobuf():
        import subprocess

        subprocess.run("protoc --proto_path=. --python_out=. ./app/protos/*.proto", shell=True)

    @app.cli.command("initdb", short_help="Create database")
    def init_db():
        # 使用 mysql docker 镜像会自动创建好 MYSQL_DATABASE 指定的数据库
        # 不需要使用这个命令来创建
        import sqlalchemy

        fe_db_uri: str = app.config["SQLALCHEMY_DATABASE_URI"]
        server_uri, database = fe_db_uri.rsplit("/", maxsplit=1)
        engine = sqlalchemy.create_engine(server_uri, echo=True)
        engine.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHAR SET 'utf8mb4'")

    # ...
    # Add more custom commands here
