import os
import json
from flask import jsonify

def get_fields_and_modules_json():
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the absolute path to the JSON file
        json_file_path = os.path.join(current_dir, '..', 'data', 'fields-modules.json')

        # Check if the file exists
        if not os.path.exists(json_file_path):
            return jsonify({"error": "JSON file not found in the data folder"}), 404

        # Load data from the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Validate if the JSON data has the expected format
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON format: expected a dictionary"}), 500

        # Return the result
        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
