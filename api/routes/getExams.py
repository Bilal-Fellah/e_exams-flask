from flask import jsonify
from api.supabase.connection import supabase
from urllib.parse import unquote

def get_exams(field_name, module_name):
    try:
        field_name =  unquote(str(field_name).lower())
        module_name = unquote(str(module_name).lower())
        
        # Use Supabase join to fetch the username from Users table
        response = supabase.table('UploadedFiles').select(
            '*, Users(full_name, score)').eq('field', field_name).eq('module', module_name).eq('is_solution', False).execute()
        
        print(response)
        if hasattr(response, 'error') and response.error:
            return jsonify({"error": f"An error occurred when getting the exams: {response.error}"}), 500
        elif not response.data:
            return jsonify({"error": "No exams found"}), 404
        else:
            return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
