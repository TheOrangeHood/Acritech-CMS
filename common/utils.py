from rest_framework import status
from rest_framework.response import Response


def custom_success_response(data):
    return Response({"status": "success", "payload": data}, status=status.HTTP_200_OK)


def custom_fail_response(data):
    return Response(
        {"status": "fail", "message": data}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
