from flask import  json, jsonify
from api.supabase.connection import supabase


def getProfileInfo(user_id):

    try:
    
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400    
        
        response = supabase.table('Users').select('*').eq('user_id', user_id).execute()

        if not response.data or len(response.data) ==0:
            return jsonify({"error": "User not found"}), 404

        return jsonify( response.data[0]), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

