from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.certificate_type_service import CertificateTypeService
from app.schemas.certificate_type import CertificateTypeCreate, CertificateTypeUpdate, CertificateTypeRead

router = APIRouter()


def get_certificate_type_service(db: AsyncSession = Depends(get_db)) -> CertificateTypeService:
    return CertificateTypeService(db=db)


@router.post(
    "/",
    response_model=CertificateTypeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new certificate type"
)
async def create_certificate_type(
    payload: CertificateTypeCreate,
    service: CertificateTypeService = Depends(get_certificate_type_service)
):
    try:
        return await service.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=list[CertificateTypeRead],
    summary="Get all certificate types"
)
async def get_certificate_types(
    service: CertificateTypeService = Depends(get_certificate_type_service)
):
    return await service.get_all()


@router.get(
    "/{type_id}",
    response_model=CertificateTypeRead,
    summary="Get a certificate type by ID"
)
async def get_certificate_type(
    type_id: int = Path(..., description="The ID of the certificate type"),
    service: CertificateTypeService = Depends(get_certificate_type_service)
):
    try:
        return await service.get_by_id(type_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/{type_id}",
    response_model=CertificateTypeRead,
    summary="Update a certificate type"
)
async def update_certificate_type(
    type_id: int = Path(..., description="The ID of the certificate type"),
    payload: CertificateTypeUpdate = ...,
    service: CertificateTypeService = Depends(get_certificate_type_service)
):
    try:
        return await service.update(type_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a certificate type"
)
async def delete_certificate_type(
    type_id: int = Path(..., description="The ID of the certificate type"),
    service: CertificateTypeService = Depends(get_certificate_type_service)
):
    try:
        await service.delete(type_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
