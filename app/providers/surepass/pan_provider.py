def verify_pan(data):

    return {
        "success": True,
        "message": "Mock PAN verification success",
        "pan_number": data.get("pan_number"),
        "candidate_name": "TEST USER",
        "pan_status": "VALID"
    }