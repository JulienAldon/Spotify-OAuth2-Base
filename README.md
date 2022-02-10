# Basic OAuth2 flow with spotify API

# Requirements
For this workshop you'll need:
- Postman (to test your app)
- Pipenv and Python 3.9+
- Docker (if you don't want to install everything on your computer)

## Create a Spotify App
https://developer.spotify.com/dashboard
Here you'll get your client secret and client id for your application

Because we are using local version for testing we are forced to redirect to `https://xxx.localhost/api/auth/login` (or any false url) to get our token

## Init db
Don't forget to initialize db (since it's a SQLite database you can init it before creating docker image)
```sh
pipenv run python initdb.py
```
## Using docker

```sh
docker build -it spotify-project-base .
```
```sh
docker run -it -p 8000:80 -e "SPOTIFY_CLIENT_ID=<client_id>" -e "SPOTIFY_CLIENT_SECRET=<client_secret>" kiki-playlist
```
## Using python (pipenv)
```sh
export SPOTIFY_CLIENT_ID=<spotify_client_id>
export SPOTIFY_CLIENT_SECRET=<spotify_client_secret>
```
```sh
pipenv install
```
```sh
pipenv run uvicorn main:app --reload
```

### Now you can get your token by pinging `/api/auth/login`
### And test the validity of your token by pinging `api/auth/user`