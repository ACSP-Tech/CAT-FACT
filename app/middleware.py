# app/middleware.py
import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/redoc", "/openapi.json", "/favicon.ico"]:
            return await call_next(request)
        
        start_time = time.time()
        
        # Log request with body for POST/PUT
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                logger.info(f"{request.method} {request.url.path} (body size: {len(body)} bytes)")
            except:
                logger.info(f"{request.method} {request.url.path}")
        else:
            logger.info(f"{request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            duration = time.time() - start_time
            
            # Different log levels based on status
            if response.status_code >= 500:
                logger.error(f"{request.method} {request.url.path} [{response.status_code}] {duration:.3f}s")
            elif response.status_code >= 400:
                logger.warning(f"{request.method} {request.url.path} [{response.status_code}] {duration:.3f}s")
            else:
                logger.info(f"{request.method} {request.url.path} [{response.status_code}] {duration:.3f}s")
            
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"{request.method} {request.url.path} FAILED after {duration:.3f}s: {str(e)}")
            raise