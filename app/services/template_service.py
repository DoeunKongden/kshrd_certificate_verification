from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.certificate_template import CertificateTemplate
from app.schemas.certificate_template import TemplateCreate, TemplateRead


class TemplateService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: TemplateCreate) -> TemplateRead:
        result = await self.db.execute(
            select(CertificateTemplate).where(CertificateTemplate.name == payload.name)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise ValueError(f"Template with name '{payload.name}' already exists")

        layout_config_data = [e.model_dump() for e in payload.layout_config]

        new_template = CertificateTemplate(
            name=payload.name,
            description=payload.description,
            layout_config=layout_config_data,
        )
        self.db.add(new_template)
        await self.db.commit()
        await self.db.refresh(new_template)

        return TemplateRead.model_validate(new_template)

    async def get_all(self) -> list[TemplateRead]:
        result = await self.db.execute(
            select(CertificateTemplate)
        )
        templates = result.scalars().all()
        return [TemplateRead.model_validate(t) for t in templates]

    async def get_by_id(self, template_id: UUID) -> TemplateRead:
        result = await self.db.execute(
            select(CertificateTemplate).where(CertificateTemplate.id == template_id)
        )
        template = result.scalar_one_or_none()
        if not template:
            raise ValueError(f"Template with id '{template_id}' not found")
        return TemplateRead.model_validate(template)
