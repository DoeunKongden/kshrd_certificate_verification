from app.services.keycloak_service import KeycloakService

_keycloak_service: KeycloakService | None = None


def get_keycloak_service() -> KeycloakService:
    global _keycloak_service
    if _keycloak_service is None:
        _keycloak_service = KeycloakService()
    return _keycloak_service
