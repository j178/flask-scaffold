def reflect_tables(db, only):
    engine = db.get_engine()
    db.metadata.bind = engine
    db.metadata.reflect(only=only)
