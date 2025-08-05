from rest_framework.response import Response
from rest_framework import status

def generate_response(data=None, message="Operation successful", status_code=status.HTTP_200_OK, errors=None, meta=None):
    """
    A utility function to generate a standardized API response.
    
    :param data: The payload or relevant data to be returned (e.g., user info, list of items).
    :param message: A concise message describing the result of the operation.
    :param status_code: The HTTP status code for the response.
    :param errors: A dictionary or list of errors (if any) for failed operations.
    :param meta: Metadata such as pagination details, links, or other contextual information.
    :return: A DRF Response object with a standardized structure.
    """
    response = {
        "status": "success" if status_code < 400 else "error",  # Automatically set status based on HTTP code
        "message": message,
        "data": data if data is not None else {},  # Ensure data is always present, even if empty
        "errors": errors if errors else [],  # Include errors only if they exist
        "meta": meta if meta else {}  # Include metadata only if it exists
    }
    return Response(response, status=status_code)