from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.certificate_type import CertificateType
from app.models.certificate_template import CertificateTemplate
from app.schemas.certificate_type import CertificateTypeCreate, CertificateTypeUpdate, CertificateTypeRead
from uuid import UUID


class CertificateTypeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payload: CertificateTypeCreate) -> CertificateTypeRead:
        if payload.template_id:
            result = await self.db.execute(
                select(CertificateTemplate).where(CertificateTemplate.id == payload.template_id)
            )
            template = result.scalar_one_or_none()
            if not template:
                raise ValueError(f"Template with id '{payload.template_id}' not found")

        new_type = CertificateType(
            name=payload.name,
            category=payload.category,
            target_role=payload.target_role,
            template_id=payload.template_id,
        )
        self.db.add(new_type)
        await self.db.commit()
        await self.db.refresh(new_type)

        return await self._to_read(new_type)

    async def get_all(self) -> list[CertificateTypeRead]:
        result = await self.db.execute(
            select(CertificateType).options(joinedload(CertificateType.template))
        )
        types = result.scalars().all()
        return [await self._to_read(t) for t in types]

    async def get_by_id(self, type_id: int) -> CertificateTypeRead:
        result = await self.db.execute(
            select(CertificateType)
            .where(CertificateType.id == type_id)
            .options(joinedload(CertificateType.template))
        )
        cert_type = result.scalar_one_or_none()
        if not cert_type:
            raise ValueError(f"CertificateType with id '{type_id}' not found")
        return await self._to_read(cert_type)

    async def update(self, type_id: int, payload: CertificateTypeUpdate) -> CertificateTypeRead:
        result = await self.db.execute(
            select(CertificateType)
            .where(CertificateType.id == type_id)
            .options(joinedload(CertificateType.template))
        )
        cert_type = result.scalar_one_or_none()
        if not cert_type:
            raise ValueError(f"CertificateType with id '{type_id}' not found")

        if payload.template_id is not None:
            if payload.template_id:
                result = await self.db.execute(
                    select(CertificateTemplate).where(CertificateTemplate.id == payload.template_id)
                )
                template = result.scalar_one_or_none()
                if not template:
                    raise ValueError(f"Template with id '{payload.template_id}' not found")
            cert_type.template_id = payload.template_id

        if payload.name is not None:
            cert_type.name = payload.name
        if payload.category is not None:
            cert_type.category = payload.category
        if payload.target_role is not None:
            cert_type.target_role = payload.target_role

        await self.db.commit()
        await self.db.refresh(cert_type)

        return await self._to_read(cert_type)

    async def delete(self, type_id: int) -> None:
        result = await self.db.execute(
            select(CertificateType).where(CertificateType.id == type_id)
        )
        cert_type = result.scalar_one_or_none()
        if not cert_type:
            raise ValueError(f"CertificateType with id '{type_id}' not found")
        
        await self.db.delete(cert_type)
        await self.db.commit()

    async def _to_read(self, cert_type: CertificateType) -> CertificateTypeRead:
        from app.schemas.certificate_type import TemplateInfo
        
        template_info = None
        if cert_type.template:
            template_info = TemplateInfo.model_validate(cert_type.template)
        
        return CertificateTypeRead(
            id=cert_type.id,
            name=cert_type.name,
            category=cert_type.category,
            target_role=cert_type.target_role,
            template_id=cert_type.template_id,
            template=template_info,
        )
