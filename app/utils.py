# Created by John Jiang at 2018/7/6 13:54


def reflect_tables(db, only):
    engine = db.get_engine()
    db.metadata.bind = engine
    db.metadata.reflect(only=only)
