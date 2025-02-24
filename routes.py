from flask import Blueprint, jsonify, request
import requests
from config import CLIENT_ID, CLIENT_SECRET
from get_access_token import get_access_token

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/search', methods=['POST'])
def search():
    album_title = request.form.get('album_title')
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    headers = {"Authorization": f"Bearer {access_token}"}
    search_url = "https://api.spotify.com/v1/search"
    search_params = {"q": album_title, "type": "album", "limit": 1}

    try:
        search_resp = requests.get(search_url, headers=headers, params=search_params)
        search_resp.raise_for_status()
        search_results = search_resp.json()
        albums = search_results.get('albums', {}).get('items', [])

        if not albums:
            return jsonify({"error": "No albums found with that title."}), 404

        selected_album = albums[0]
        album_id = selected_album['id']
        album_name = selected_album['name']

        tracks_url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
        tracks_resp = requests.get(tracks_url, headers=headers)
        tracks_resp.raise_for_status()
        tracks_data = tracks_resp.json()
        tracks = [track['name'] for track in tracks_data['items']]

        return jsonify({"album_name": album_name, "tracks": tracks})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data from Spotify API."}), 500
