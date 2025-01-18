import pandas as pd
import json
import uuid
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

def excel_to_json(file_path):
    
    df = pd.read_excel(file_path)
    
    base_keys = [
        "requestId", "userId", "firstName", "lastName",
        "emailId", "mobileNo", "mobile_extension",
        "dob", "title", "gender"
    ]
    extra_fields_keys = ["cost_centre", "cost_category", "designation", "department"]
    
    data = []

    
    for _, row in df.iterrows():
        first_name = str(row.get("First Name", "")) or ""
        last_name = str(row.get("Last Name", "")) or ""
        
        
        email = row.get("Email", f"{first_name.lower()}.{last_name.lower()}@happy.in")
        mobile = str(row.get("Mobile", ""))
        dob = row.get("Date of Birth", "")
        title = "Mr." if row.get("Gender", "").lower() == "male" else "Ms."
        gender = row.get("Gender", "")
        
        
        if isinstance(dob, pd.Timestamp):
            dob = dob.strftime('%Y-%m-%d')
        else:
            dob = ""  

        
        json_object = {
            "requestId": str(uuid.uuid4()),  
            "userId": f"usr_{uuid.uuid4().hex}",
            "firstName": first_name,
            "lastName": last_name,
            "emailId": email,
            "mobileNo": mobile if mobile else "N/A",
            "mobile_extension": "+91",
            "dob": dob,
            "title": title,
            "gender": gender,
            "extra_fields": {
                "cost_centre": row.get("Cost Centre", ""),
                "cost_category": row.get("Cost Category", ""),
                "designation": row.get("Designation", ""),
                "department": row.get("Department", "")
            }
        }
        data.append(json_object)

    
    return jsonify(data)

@app.route('/get_users', methods=['GET'])
def get_users():
    
    file_path = "/Users/vineeta.s/Documents/sample_excel_file_integration.xlsx"
    return excel_to_json(file_path)

if __name__ == '__main__':
    app.run(debug=True)
