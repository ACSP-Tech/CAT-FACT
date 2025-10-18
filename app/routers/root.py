from fastapi import APIRouter, Response

router = APIRouter(tags=["Root"])

# Render liveness check
@router.get("/")
async def root():
    """
    root endpoint
    """
    return {"app_name": "random cat fact",
            "redoc": "https://acsp-cat-fact.pxxl.click/redoc"}

@router.head("/")
async def root_head():
    """
    head health check endpoint
    """
    return Response(status_code=200)