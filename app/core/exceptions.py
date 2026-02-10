"""
Core Exception Registry

This module defines custom business logic exceptions for the application. 
Following the 'Fail Fast' principle, the service layer should raise these 
exceptions to be caught and handled by the API route layer or a global 
exception handler.

Usage:
    raise CertificateNotFoundError(code="CERT-123")
"""


class AppBaseException(Exception):
    """Base class for all application-specific exceptions."""
    pass


class CertificateNotFoundError(AppBaseException):
    """
    Raised when a requested certificate verification code does not exist.
    
    Attributes:
        code -- the verification code that was not found
    """
    def __init__(self, code: str):
        self.code = code
        self.message = f"Certificate with verification code '{code}' does not exist."
        super().__init__(self.message) # passes self.message to parent exception class
    


class CertificateInActiveError(AppBaseException):
    """
    Raised when a certificate exists but its 'is_active' status is False.
    
    Attributes:
        message -- explanation of why the certificate is considered inactive
    """

    def __init__(self, message: str="This certificate is no longer active or has been revoked."):
        self.message = message
        super().__init__(self.message)