from .models import *
from datetime import datetime
from sqlalchemy.ext.asyncio.session import AsyncSession



async def create_report(session: AsyncSession, report_create: CreateReportFull) -> Report:
    report = Report.model_validate(
        report_create
    )
    session.add(report)
    await session.commit()
    await session.refresh(report)

    return report
