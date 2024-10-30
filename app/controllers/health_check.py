from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.config.database import db_connection


router = APIRouter(
    prefix="/health-check",
    tags=["Health Check"]
)


@router.get("/api")
async def api_health_check():
    return {"status": "ok"}


@router.get("/db")
async def db_health_check(db: Session = Depends(db_connection)):
    query = text("SELECT * FROM alembic_version")
    result = db.execute(query, ).all()

    migration_versions = [{"version": row[0]} for row in result]

    print(migration_versions, type(migration_versions))

    return {
        "status": "ok",
        "migration_versions": migration_versions
    }
