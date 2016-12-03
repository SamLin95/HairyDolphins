if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from webapp.models.models import db
import boto
"""The tool will remove all data, schemas and files stored on S3 and recreate the database"""

#Drop all current data and schema.
db.engine.execute("DROP SCHEMA IF EXISTS public CASCADE")
#Create schema again
db.engine.execute("CREATE SCHEMA public;GRANT ALL ON SCHEMA public TO postgres;GRANT ALL ON SCHEMA public TO public;")

#Steps to recreate database on remote server
db.configure_mappers()
db.create_all()
db.session.commit()

# delete all keys in buckets in amazon s3
keys = boto.connect_s3().get_bucket('hairydolphins').get_all_keys()
for key in keys:
	key.delete()

