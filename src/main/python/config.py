import os
"""All flask app configurations should be stored here"""
SECRET_KEY = os.urandom(24)
UPLOAD_FOLDER = '/tmp'
