import bottle
import requests
from fibi.db import User
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode

from fibi.main import app


@app.get("/auth")
def auth_start():
    base_url = "https://www.fitbit.com/oauth2/authorize"
    query = {
        "client_id": app.config["oauth2.client_id"],
        "response_type": "code",
        "scope": "heartrate",
        "redirect_uri": "http://localhost:8080/auth_callback",
    }
    path = base_url + "?" + urlencode(query)
    bottle.redirect(path)


@app.get("/auth_callback")
def auth_start(db):
    code = bottle.request.query.code
    token_url = "https://api.fitbit.com/oauth2/token"
    post_data = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": app.config["oauth2.client_id"],
        "redirect_uri": "http://localhost:8080/auth_callback",
    }
    result = requests.post(
        token_url,
        data=post_data,
        auth=HTTPBasicAuth(
            app.config["oauth2.client_id"], app.config["oauth2.client_secret"]
        ),
    )
    access_data = result.json()
    user = User(
        fitbit_user_id=access_data["user_id"],
        access_token=access_data["access_token"],
        refresh_token=access_data["refresh_token"],
    )
    db.merge(user)
