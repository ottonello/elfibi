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
        "scope": "activity heartrate location nutrition profile settings sleep social weight",
        "redirect_uri": f"{app.config['api.root']}/auth_callback",
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
        "redirect_uri": f"{app.config['api.root']}/auth_callback",
    }
    result = requests.post(
        token_url,
        data=post_data,
        auth=HTTPBasicAuth(
            app.config["oauth2.client_id"], app.config["oauth2.client_secret"]
        ),
    )
    access_data = result.json()
    user_id = access_data["user_id"]
    user = User(
        fitbit_user_id=user_id,
        access_token=access_data["access_token"],
        refresh_token=access_data["refresh_token"],
    )
    db.merge(user)
    bottle.response.set_cookie("user_id", user_id)
    # return f"Hello there! Nice to meet you {user_id}"
    bottle.redirect(f"{app.config['app.root']}/")



def refresh_token(db, user):
    token_url = "https://api.fitbit.com/oauth2/token"
    post_data = {
        "refresh_token": user.refresh_token,
        "grant_type": "authorization_code"
    }
    result = requests.post(
        token_url,
        data=post_data,
        auth=HTTPBasicAuth(
            app.config["oauth2.client_id"], app.config["oauth2.client_secret"]
        ),
    )
    access_data = result.json()
    user_id = access_data["user_id"]
    user = User(
        fitbit_user_id=user_id,
        access_token=access_data["access_token"],
        refresh_token=access_data["refresh_token"],
    )
    db.merge(user)
    bottle.response.set_cookie("user_id", user_id)


# @app.get("/heart/<date:re[0-1]{4}-re[0-1]{2}-re[0-1]{2}>")
@app.get("/heart/<date>")
def heart_today(db, date):
    print(date)
    user_id = bottle.request.get_cookie("user_id")
    if not user_id:
        print("Cookie not found")
        bottle.abort(401)
    user = db.query(User).get(user_id)
    if not user:
        print("User not found")
        bottle.abort(401)
    print(user)
    # To make a request to the Fitbit API using OAuth 2.0, simply add an Authorization header to the HTTPS request with the
    # user's access token.
    #GET https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json
    #/1/user/-/activities/heart/date/today/1d.json
    heart_rate_today = f"https://api.fitbit.com/1/user/{user_id}/activities/heart/date/{date}/1d.json"
    url = heart_rate_today.format(user_id=user.fitbit_user_id)
    print(f"Requesting {url}")
    result = requests.get(url, headers={"Authorization": f"Bearer {user.access_token}" })
    print(result.json())
    if result.status_code == 401:
        json_result = result.json()
        if 'errors' in json_result and json_result["errors"][0]["errorType"] == "expired_token":
            print("refresh token!")
            refresh_token(db, user)
        else:
            bottle.abort(401)
    return result.json()