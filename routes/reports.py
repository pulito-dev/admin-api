from .. import crud
from ..models import *
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from .deps import get_session, get_current_user, get_accommodation_by_id


reports_router = APIRouter()


@reports_router.get("/")
async def get_all_reports(session: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user))  -> ReportsPublic:

    if str(current_user.get("role").get("name")).lower() != "admin":
        raise HTTPException(
            status_code=401,
            detail="Only for admins"
        )

    statement = select(Report)
    res = await session.execute(statement)
    reports = res.scalars().all()
    
    return ReportsPublic(data=reports)


@reports_router.post("/")
async def create_report( create_report: CreateReport, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)) -> CreateReportPublic:

    accommodation: dict = await get_accommodation_by_id( create_report.accommodation_id)

    if not accommodation:
        raise HTTPException(
            status_code=404,
            detail=f"Accommodation with id { create_report.accommodation_id} does not exist"
        )
    
    # cannot report your own accommodation
    if accommodation.get("user_id") == current_user.get("id"):
        raise HTTPException(
            status_code=400,
            detail="You cannot report your own accommodation"
        )
    
    create_report = CreateReportFull(
        accommodation_id=create_report.accommodation_id,
        user_id=current_user.get("id")
    )
    

    report = await crud.create_report(session,  create_report)

    return CreateReportPublic(
        id=report.id,
        msg="Report created successfully"
    )

