import token
from typing import Optional

from fastapi import Depends, security
from fastapi.dependencies.models import Dependant
import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

from app.core.config import settings

# HTTPBearer extracts "Bearer <token>" from authorization header
# auto_error=False lets us return a custom 401 message
security = HTTPBearer(auto_error=False)

# PyJWTClient fetches the JWKS from Keycloak and caches keys (handle rotation)
_jwks_client = Optional[PyJWKClient] = None


def get_jwks_client() -> PyJWKClient:
    """Lazy-initialize the JWKS client (fetches/caches Keycloak public key)"""
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = PyJWKClient(
            uri=settings.JWKS_URL,
            cache_keys=True,
            cache_jwk_set=True,
            lifespan=3600,
        )
    return _jwks_client


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """
    FastAPI dependency that verifies the JWT and returns the tokenb payload.
    Use as: current_user: dict = Depends(get_current_user)
    """

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    try:
        # 1. Get the signing key from JWKS (matches token's 'kid' in header)
        jwks_client = get_jwks_client()
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # 2. Verify and decode the token
        # - algorithms: MUST specify RS256 (prevents algorithm confusion attacks)
        # - options: validate exp (expiration) by default
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
            },
            audience=settings.KEYCLOAK_CLIENT_ID,  # Optional: validate token was issued for your client
            issuer=f"{settings.KEYCLOAK_URL.rstrip('/')}/realms/{settings.KEYCLOAK_REALM}",
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
