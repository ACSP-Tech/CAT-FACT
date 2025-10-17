from fastapi import APIRouter, Response

router = APIRouter(tags=["Root"])

# Render liveness check
@router.get("/")
async def root():
    """
    root endpoint
    """
    return {"app_name": "random cat fact",
            "redoc": "/redoc"}

@router.head("/")
async def root_head():
    """
    head health check endpoint
    """
    return Response(status_code=200)