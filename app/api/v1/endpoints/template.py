from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.auth import get_current_user
from app.db.database import get_db
from app.services.template_service import TemplateService
from app.schemas.certificate_template import TemplateCreate, TemplateRead, TemplateUpdate

router = APIRouter()

def get_template_service(db: AsyncSession = Depends(get_db)) -> TemplateService:
    return TemplateService(db=db)


@router.post(
    "/",
    response_model=TemplateRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new certificate template"
)
async def create_template(
    payload: TemplateCreate,
    current_user: dict = Depends(get_current_user),
    service: TemplateService = Depends(get_template_service)
):
    try:
        return await service.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=list[TemplateRead],
    summary="Get all certificate templates"
)
async def get_templates(
    current_user: dict = Depends(get_current_user),
    service: TemplateService = Depends(get_template_service)
):
    return await service.get_all()


@router.get(
    "/{template_id}",
    response_model=TemplateRead,
    summary="Get a certificate template by ID"
)
async def get_template(
    template_id: UUID = Path(..., description="The UUID of the template"),
    current_user: dict = Depends(get_current_user),
    service: TemplateService = Depends(get_template_service)
):
    try:
        return await service.get_by_id(template_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/{template_id}",
    response_model=TemplateRead,
    summary="Update a certificate template"
)
async def update_template(
    template_id: UUID = Path(..., description="The UUID of the template"),
    payload: TemplateUpdate = ...,
    current_user: dict = Depends(get_current_user),
    service: TemplateService = Depends(get_template_service)
):
    try:
        return await service.update(template_id, payload)
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{template_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a certificate template"
)
async def delete_template(
    template_id: UUID = Path(..., description="The UUID of the template"),
    current_user: dict = Depends(get_current_user),
    service: TemplateService = Depends(get_template_service)
):
    try:
        await service.delete(template_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))