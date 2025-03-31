from flask import Blueprint, jsonify, request
from flask_cors import CORS
import json, requests

leaderboard_bp = Blueprint('leaderboard', __name__)


@leaderboard_bp.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """
    Fetch the current F1 leaderboard from the API and return it as JSON.
    This one is currently depreicated and will be removed in the future. 
    Currently for testing purposes only.
    """
    try:
        # Make a request to the F1 API to get the current leaderboard
        response = requests.get('https://ergastatapi.com/api/f1/current/driverStandings.json')
        data = response.json()

        # Extract relevant information from the response
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

        # Format the data for easier consumption
        formatted_standings = [
            {
                'position': standing['position'],
                'driver': f"{standing['Driver']['givenName']} {standing['Driver']['familyName']}",
                'points': standing['points'],
                'team': standing['Constructors'][0]['name']
            }
            for standing in standings
        ]

        return jsonify(formatted_standings), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500