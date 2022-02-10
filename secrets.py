import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:8000',
]
REDIRECT  = 'https://xxx.localhost/api/auth/authorized'
ROOT_FQDN = 'http://localhost:8080'

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SCOPES    = '+'.join((
'playlist-read-private',
'playlist-modify-private',
'playlist-modify-public',
'playlist-read-collaborative',
))
