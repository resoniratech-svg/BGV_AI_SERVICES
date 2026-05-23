def verify_aadhaar(data):

    return {
        "success": True,
        "message": "Aadhaar verification placeholder",
        "data": data
    }
def verify_aadhaar(data):

    return {
        "success": True,
        "message": "Mock Aadhaar verification success",
        "aadhaar_number": data.get("aadhaar_number"),
        "candidate_name": "TEST USER",
        "aadhaar_status": "VALID"
    }