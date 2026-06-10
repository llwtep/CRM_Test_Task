class ServiceException(Exception):
    """Base class for service-related exceptions."""
    pass

class NotFoundException(ServiceException):
    """Raised when a requested resource is not found."""
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)

class ValidationException(ServiceException):
    """Raised when business logic validation fails."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
