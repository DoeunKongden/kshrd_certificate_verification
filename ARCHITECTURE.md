📜 System Architecture & Development Context
🎯 Project Goal
A high-integrity Certificate Verification System that provides a Role-Based Experience. The system must distinguish between STUDENT and STAFF personas to render different UI layouts and data sets upon verification.

🏗️ Core Architecture (The "Pillars")
Identity: Managed via Keycloak (stored as user_id UUID in Postgres).

Verification: Triggered by a unique verify_code in the certificates table.

The Switch (Feature #1): CertificateType.target_role determines the persona.

The UI (Feature #2): CertificateTemplate (UUID-based) stores the layout configuration (colors, themes) in layout_config (JSONB).

📂 Database Schema Mapping (Source of Truth)
The AI should prioritize these relationships:

Certificate -> CertificateType (via type_id)

CertificateType -> CertificateTemplate (via template_id UUID)

Certificate -> Subject -> Topic (Academic data for STUDENT role)

🛠️ Development Guidelines for AI Agent
1. Data Integrity & Types
UUIDs: Always use native PostgreSQL UUIDs for certificates.id, certificate_templates.id, and user_id.

Joins: When fetching a certificate for verification, always use Eager Loading (joinedload) for type and template to avoid N+1 queries.

2. Logic Branching (The "Persona" Logic)
When writing service logic, follow this flow:

Python
if certificate.type.target_role == "STUDENT":
    # Include curriculum, subjects, and topics
elif certificate.type.target_role == "STAFF":
    # Include professional milestones (Future implementation)
3. API Response Contract
The response must be "Hydrated." It should not just return IDs; it must return the template_name and the target_role so the frontend knows which component to mount.

🚫 Constraints & Rules
No Hardcoding: Do not hardcode Template IDs. Always query by name or UUID.

Database First: The database is already restructured in pgAdmin. Ensure all SQLAlchemy models strictly match the models/ directory.

Modular Models: Keep models separated (e.g., certificate_type.py is distinct from certificate.py).