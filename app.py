import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, redirect, render_template

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    artist_name = request.form["artist_name"]
    access_token = get_access_token()

    if access_token:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        url = f"https://api.spotify.com/v1/search?q={artist_name}&type=album&market=ES"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            albums = data["albums"]["items"]
            return render_template("search.html", albums=albums)

    return redirect("/")

def get_access_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        return None

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        data = response.json()
        access_token = data["access_token"]
        return access_token

    return None

if __name__ == "__main__":
    app.run(debug=True)