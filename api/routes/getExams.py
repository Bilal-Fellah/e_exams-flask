from flask import jsonify
from api.supabase.connection import supabase

def get_exams(field_name, module_name):
    try:
        field_name = str(field_name).lower()
        module_name = str(module_name).lower()
    
        response = supabase.table('UploadedFiles').select('*').eq('field', field_name).eq('module', module_name).execute()
           
        
        # if not response.data:
        #     return jsonify({"error": f"No exams found{response}"}), 404
        if hasattr(response, 'error'):
            return jsonify({"error": f"an error occured when getting the exams:{response.error}"})
        else:
            return jsonify(response.data), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 500