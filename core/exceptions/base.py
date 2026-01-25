from fastapi import HTTPException, status


class CustomException(HTTPException):
    """
    Base class for all custom HTTP exceptions.

    HTTP Status: Varies
    """

    def __init__(self, message: str, code: int = status.HTTP_502_BAD_GATEWAY):
        super().__init__(status_code=code, detail=message)


class BadRequestException(CustomException):
    """
    Raised when the request data is invalid or malformed.

    HTTP Status: 400 Bad Request
    """

    def __init__(self, message: str = "Bad Request"):
        super().__init__(message, code=status.HTTP_400_BAD_REQUEST)


class NotFoundException(CustomException):
    """
    Raised when the requested resource does not exist.

    HTTP Status: 404 Not Found
    """

    def __init__(self, message: str = "Not Found"):
        super().__init__(message, code=status.HTTP_404_NOT_FOUND)


class ForbiddenException(CustomException):
    """
    Raised when the client lacks permission to access the resource.

    HTTP Status: 403 Forbidden
    """

    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, code=status.HTTP_403_FORBIDDEN)


class UnauthorizedException(CustomException):
    """
    Raised when authentication is missing or invalid.

    HTTP Status: 401 Unauthorized
    """

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, code=status.HTTP_401_UNAUTHORIZED)


class UnprocessableEntityException(CustomException):
    """
    Raised when the request is syntactically valid but semantically incorrect.

    HTTP Status: 422 Unprocessable Entity
    """

    def __init__(self, message: str = "Unprocessable Entity"):
        super().__init__(message, code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class DuplicateValueException(UnprocessableEntityException):
    """
    Raised when a duplicate or unique constraint violation occurs.

    HTTP Status: 422 Unprocessable Entity
    """

    def __init__(self, message: str = "Duplicate value found"):
        super().__init__(message)


class InternalServerErrorException(CustomException):
    """
    Raised when an unexpected internal server error occurs.

    HTTP Status: 500 Internal Server Error
    """

    def __init__(self, message: str = "Internal Server Error"):
        super().__init__(message, code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BadGatewayException(CustomException):
    """
    Raised when an upstream service returns an invalid response.

    HTTP Status: 502 Bad Gateway
    """

    def __init__(self, message: str = "Bad Gateway"):
        super().__init__(message, code=status.HTTP_502_BAD_GATEWAY)


class ServiceUnavailableException(CustomException):
    """
    Raised when the service is temporarily unavailable.

    HTTP Status: 503 Service Unavailable
    """

    def __init__(self, message: str = "Service Unavailable"):
        super().__init__(message, code=status.HTTP_503_SERVICE_UNAVAILABLE)


class GatewayTimeoutException(CustomException):
    """
    Raised when an upstream service times out.

    HTTP Status: 504 Gateway Timeout
    """

    def __init__(self, message: str = "Gateway Timeout"):
        super().__init__(message, code=status.HTTP_504_GATEWAY_TIMEOUT)
