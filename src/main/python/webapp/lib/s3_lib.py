import os
import boto
import boto.s3
import sys
from boto.s3.key import Key

#TODO: To be stored in separate files
AWS_ACCESS_KEY_ID = 'AKIAIRNR57AQD5F7EEJA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_S3_BUCKET_NAME = 'hairydolphins'

class S3Helper():
    def __init__(self):
        conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(AWS_S3_BUCKET_NAME)
        self.bucket = bucket

    def upload_file(self, local_file_name, remote_filename):
        key = boto.s3.key.Key(self.bucket, remote_filename)
        with open(local_file_name) as fp:
            key.set_contents_from_file(fp)
            key.set_acl('public-read')

