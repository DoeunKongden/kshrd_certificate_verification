from typing import Optional
from uuid import UUID
from keycloak import KeycloakAdmin, KeycloakError
from app.core.config import settings
from ..schemas.user import UserProfile


class KeycloakService:
    """Class for managing all Keycloak services and connections"""

    def __init__(self):
        # Inititalize the connections to the admin API
        self.admin = KeycloakAdmin(
            server_url=settings.KEYCLOAK_URL,
            realm_name=settings.KEYCLOAK_REALM,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
            grant_type="client_credentials",
        )

    def _extract_attribute(
        self, attributes: dict, key: str, default: Optional[str] = None
    ) -> Optional[str]:
        """
        Helper method for extracting attribute value from the Keycloak attribute dict.
        """
        if key not in attributes:
            return default

        attr_value = attributes[key]
        if isinstance(attr_value, list) and len(attr_value) > 0:
            return attr_value[0]
        elif attr_value:
            return str(attr_value)
        return default

    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Fetches the user from Keycloak admin api and maps it to the UserProfile Pydantic Model
        """
        try:
            user_data = self.admin.get_user(user_id=user_id)

            if not user_data:
                return None

            # Getting a specific attribute from the user
            user_attributes = user_data.get("attributes", {})
            photo_url = None
            for attr_name in [
                "profile_image",
                "profileImage",
                "photo_url",
                "profile-image",
                "Profile Image",
            ]:
                if attr_name in user_attributes:
                    photo_url = self._extract_attribute(user_attributes, attr_name)
                    break

            roles = []
            if "realmRoles" in user_data:
                roles.extend(user_data["realmRoles"])
            if "clientRoles" in user_data:
                for client_roles in user_data["clientRoles"].values():
                    roles.extend(client_roles)

            return UserProfile(
                id=UUID(user_data["id"]),
                username=user_data.get("username", ""),
                email=user_data.get("email"),
                full_name_en=f"{user_data.get('firstName', '')} {user_data.get('lastName', '')}".strip()
                or user_data.get("username", ""),
                photo_url=photo_url,
                roles=roles,
                # Extract all custom attributes
                phone_number=self._extract_attribute(user_attributes, "phone-number"),
                address=self._extract_attribute(user_attributes, "address"),
                gender=self._extract_attribute(user_attributes, "gender"),
                university=self._extract_attribute(user_attributes, "university"),
                bacll_grade=self._extract_attribute(user_attributes, "bacll-grade"),
                khmer_name=self._extract_attribute(user_attributes, "khmer-name"),
                province=self._extract_attribute(user_attributes, "province"),
                dob=self._extract_attribute(user_attributes, "dob"),
                education_level=self._extract_attribute(
                    user_attributes, "education-level"
                ),
            )

        except KeycloakError as e:
            error_msg = str(e)
            if "403" in error_msg or "Forbidden" in error_msg:
                raise PermissionError(
                    f"Keycloak Permission Denied (403): The client '{settings.KEYCLOAK_CLIENT_ID}' "
                    f"does not have permission to read users. Please assign the 'view-users' role "
                    f"from the 'realm-management' client to the service account."
                ) from e
            elif "404" in error_msg or "Not Found" in error_msg:
                return None  # User doesn't exist
            else:
                raise RuntimeError(f"Keycloak API Error: {error_msg}") from e

        except Exception as e:
            print(f"Keycloak Fetch Error: {str(e)}")
            return None
