from flask import jsonify
from api.supabase.connection import supabase

def do_update_score(user_id, score):

    try:
        # return {"success":"asdfasdfjjjjjjj"}

        # Fetch the user's current score
        user_data = supabase.table("Users").select("score").eq("user_id", user_id).execute()
        # return user_data
        if not user_data.data:
            return jsonify({"error": "User not found"}), 404
        
        # Get the current score
        current_score = user_data.data[0]["score"]
        
        # Add the new score to the current score
        new_score = current_score + score

        # Update the user's score in the database
        update_response = supabase.table("Users").update({"score": new_score}).eq("user_id", user_id).execute()
        if hasattr(update_response, 'error'):
            return jsonify({"error": f"Failed to update score: {update_response.error}"}), 500
        
        else:
            return jsonify({
                "message": "Score updated successfully",
                "user_id": user_id,
                "new_score": new_score
            }), 200
           
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500