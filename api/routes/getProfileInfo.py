from flask import  json, jsonify

profiles = {
    1: {
        "image": 'assets/images/profile1.jpg',
        "role": '3rd year CS student',
        "full_name": 'John Doe',
        "email": 'johndoe@example.com',
        # "value": '+1 234 567 890',
        # "linkedin": 'linkedin.com/in/johndoe',
        "score": 250,
    },
    2: {
        "image": 'assets/images/profile2.jpg',
        "role": '2nd year IT student',
        "full_name": 'Jane Smith',
        "email": 'janesmith@example.com',
        # "ph": '+1 987 654 321',
        # "linkedin": 'linkedin.com/in/janesmith',
        "score": 300,
    },
    # Add more profiles as needed
}


# @app.route("/api/files", methods=["GET"])
def getProfileInfo(user_id):
    
    profile = profiles.get(user_id)  # Fetch the profile by ID
    if profile:
        return jsonify(profile)  # Return the profile if found
    else:
        return jsonify({"error": "User not found"}), 404  # Return 404 if the user doesn't exist

