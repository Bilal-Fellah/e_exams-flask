from flask import jsonify
from api.supabase.connection import supabase

def get_fields_and_modules():
    try:
        # Fetch all rows from the UploadedFiles table
        response = supabase.table('UploadedFiles').select('field, module').execute()

        # Check for errors in the response
        if hasattr(response, 'error') and response.error:
            return jsonify({"error": f"An error occurred when fetching fields and modules: {response.error}"}), 500

        # Extract data
        data = response.data
        if not data:
            return jsonify({"error": "No data found"}), 404

        # Organize fields and their associated modules
        fields_and_modules = {}
        for row in data:
            field = row['field'].lower()
            module = row['module'].lower()

            if field not in fields_and_modules:
                fields_and_modules[field] = []

            if module not in fields_and_modules[field]:
                fields_and_modules[field].append(module)

        # Return the result as a JSON response
        return jsonify(fields_and_modules), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
