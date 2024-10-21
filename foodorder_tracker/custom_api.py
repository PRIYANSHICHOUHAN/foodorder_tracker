import frappe
import requests

@frappe.whitelist()
def get_pending_meals(month):
    url = 'http://canteen.benzyinfotech.com/api/v3/customer/report'
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZWRhNWExODU0OTFhYWE0MmY5YzMyZjRhMTU5MDM1ODk4ZjZiMzMxNWUzZjJjNGRiZDA1N2IyNGE3NTAzMDc3NDBlMjFlYjZmNGE4Mjk0MGUiLCJpYXQiOjE3MDQ4MDA4OTAuODc5OTI1OTY2MjYyODE3MzgyODEyNSwibmJmIjoxNzA0ODAwODkwLjg3OTkyOTA2NTcwNDM0NTcwMzEyNSwiZXhwIjoxNzM2NDIzMjkwLjgzNDkxMjA2MTY5MTI4NDE3OTY4NzUsInN1YiI6IjI2NSIsInNjb3BlcyI6W119.CwDEjlHoRtOXdFcaO6KGGxV202AOA7MMtJVPtKzgLqzTFzUUnDLGBd7PNAtHO2--3YOathM9HOG8hYjY8wjktXZIoCGUR9GWIaEVUxLwFq927CrSf05NuqTBTrJcDeBOjXDvKcSBiJ2A994FC2IunPcdkaZ4jpoaWBIaWueYUbHviYSQuLec3tFcAMg4njrImAlaN9k-QKkHetpdrdbUEX1Wzq4X-1QwuOx7W3W2nbbxaoNgFX1gaabxi00ZO7h5MokGvtqy_gCkS9TYoM74VfxmTyAAczjttLcPqDNiAL_ZJdutDMezw32CZj8G8l8PUL46F_BuaxatZDBUZxeClZh4_0Wvo9GX4zqF2XvHdzZHnwdB414vNCl8itaGW9w7QWbdchPOglhnek32ZmkH0MIqeOBhnAyHo5_WbP0uLd_3qmz3w04nvTbTGV25-QebaxPAsVD0-7Za1sVpqB_FD6yEeliaEzdxl_8gA5IH59uowpfPYgUIjom8NVEASuYsAwb0q3f0jhNRfwg2zmXNenoDunh_dN9l2NRjI2gdZueSMwu6IJLQK46jpn01uG2iQ1xx-pFJAGe_bzSceLsho3dbtabym3tMqi0Ac02xUP9Mn50LdkFJGNVU9jiuHQfyjQirDtGUfya3aIvpJlCGx9Cx99s_4P89uDnOiXy3A1Q',
    'Content-Type': 'application/json',
    'Cookie': 'XSRF-TOKEN=your_token; canteen_session=your_session'  
    }

    data = {
        "month": int(month)  
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            reports = response.json().get('reports', [])
            total_pending_amount = 0
            pending_meals = []

            # Process each report
            for report in reports:
                employee_name = report.get('employee_name', 'Unknown')
                date = report.get('date', '')
                opt_ins = report.get('opt_ins', {})

                if isinstance(opt_ins, dict):
                    # Calculate fine for pending meals
                    pending_count = sum(1 for status in opt_ins.values() if status == "Pending")
                    fine_amount = pending_count * 100

                    # Add to total fine
                    total_pending_amount += fine_amount

                    # Append to pending meals list
                    pending_meals.append({
                        'date': date,
                        'breakfast': opt_ins.get('breakfast', 'N/A'),
                        'lunch': opt_ins.get('lunch', 'N/A'),
                        'dinner': opt_ins.get('dinner', 'N/A'),
                        'fine_amount': fine_amount
                    })

            return {
                'pending_meals': pending_meals,
                'total_pending_amount': total_pending_amount
            }

        else:
            return {'error': f"API Error {response.status_code}: {response.text}"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'API Request Failed')
        return {'error': str(e)}