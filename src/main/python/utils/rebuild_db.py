if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from webapp.models.models import db

db.engine.execute("DROP SCHEMA IF EXISTS public CASCADE")
db.engine.execute("CREATE SCHEMA public;GRANT ALL ON SCHEMA public TO postgres;GRANT ALL ON SCHEMA public TO public;")
db.configure_mappers()
db.create_all()
db.session.commit()
