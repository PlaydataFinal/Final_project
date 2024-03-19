#mysettings.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MYDATABASE_ROUTERS = [
    'mysite.dbrouter.MultiDBRouter',
]

MYDATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     },

    'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME':  'final',
                'USER':  'admin',
                'PASSWORD' : '1q3w3e9q9q7!@',
                'HOST' : '3.34.79.5',
                'PORT':  '3306'
            },
    
    'mongo': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': False,
        'NAME': 'jejutext',
        'CLIENT': {
            'host': 'mongodb+srv://admin:admin123@atlascluster.rlgup9y.mongodb.net/jejutext',
            'username': 'admin',
            'password': 'admin123',
            'authMechanism': 'SCRAM-SHA-1',
            'retryWrites': True,
            'w': 'majority',
            'appName': 'AtlasCluster',
        }
    }
}