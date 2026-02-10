from ..db.database import Base
from .generation import Generation
from .user import User
from .curriculum import Subject, Topic
from .certificate import Certificate, CertificateType

# This list makes it easy to see all your entities in one place
__all__ = [
    "Base", 
    "Generation", 
    "User", 
    "Subject", 
    "Topic", 
    "Certificate", 
    "CertificateType"
]