from flask import Flask, json, jsonify




# @app.route("/api/files", methods=["GET"])
def get_files():
    try:
        # Open and load the JSON file
        with open("api/data/fields-modules.json", "r") as file:
            data = json.load(file)
        return jsonify(data)  # Return the JSON data as a response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
