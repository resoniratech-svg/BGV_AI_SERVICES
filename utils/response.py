def success_response(data=None, message="Success", status=200):

    return {
        "success": True,
        "message": message,
        "data": data
    }, status


def error_response(message="Error", status=500):

    return {
        "success": False,
        "message": message
    }, status