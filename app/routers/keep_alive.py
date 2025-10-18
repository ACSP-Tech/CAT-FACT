# app/routes/keepalive.py
from fastapi import APIRouter, Header, HTTPException, status, Depends
from sqlalchemy import text
from ..database_setup import get_db
from ..sec import KEEP_ALIVE_TOKEN

router = APIRouter(tags=["Keep Alive"])

@router.get("/internal/keepalive")
async def keepalive(session=Depends(get_db)):
    await session.execute(text("SELECT 1"))
    return {"ok": True}

# Cron-job.org keep-alive
@router.get("/cron")
async def cron_job():
    return {"status": "cron triggered"}