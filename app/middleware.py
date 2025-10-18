import logging
import time
import json
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import uuid
from datetime import datetime, timezone
from decouple import config

cloud_env = config("CLOUD_ENV", default=False, cast=bool)

def setup_logging():
    """Setup logging configuration based on environment"""
    log_level = config("LOG_LEVEL", "INFO").upper()

    # For cloud deployments, only use console logging
    if  cloud_env:
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler()  # Console only for cloud
            ],
            force=True  # Override any existing logging config
        )
    else:
        # Local development - use both file and console
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('bookify.log'),
                logging.StreamHandler()
            ],
            force=True
        )


# Initialize logging
setup_logging()

logger = logging.getLogger("Bookify_api")


class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all HTTP requests and responses
    """

    def __init__(self, app, log_body: bool = True, max_body_size: int = 1024):
        """
        Initialize the middleware

        Args:
            app: FastAPI application instance
            log_body: Whether to log request/response bodies
            max_body_size: Maximum size of body to log (in bytes)
        """
        super().__init__(app)
        self.log_body = log_body
        self.max_body_size = max_body_size

        # Endpoints to exclude from logging (to reduce noise)
        self.exclude_paths = {
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico",
            "/health"  # Add health check endpoint if you have one
        }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate unique request ID for tracing
        request_id = str(uuid.uuid4())[:8]

        # Skip logging for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Record start time
        start_time = time.time()

        # Log request
        await self._log_request(request, request_id)

        # Process the request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        await self._log_response(response, request_id, process_time)

        return response

    async def _log_request(self, request: Request, request_id: str):
        """Log incoming request details"""
        try:
            # Basic request info
            request_info = {
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "query_params": dict(request.query_params) if request.query_params else None,
                "client_ip": self._get_client_ip(request)
            }

            # Log request body if enabled and appropriate
            if self.log_body and request.method in ["POST", "PUT", "PATCH"]:
                try:
                    body = await request.body()
                    if body and len(body) <= self.max_body_size:
                        # Try to parse as JSON for better formatting
                        try:
                            request_info["body"] = json.loads(body.decode())
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            request_info["body"] = body.decode('utf-8', errors='ignore')[:self.max_body_size]
                    elif len(body) > self.max_body_size:
                        request_info["body"] = f"<Body too large: {len(body)} bytes>"
                except Exception as e:
                    request_info["body_error"] = f"Could not read body: {str(e)}"

            logger.info(f"INCOMING REQUEST: {json.dumps(request_info, indent=2)}")

        except Exception as e:
            logger.error(f"Error logging request {request_id}: {str(e)}")

    async def _log_response(self, response: Response, request_id: str, process_time: float):
        """Log outgoing response details"""
        try:
            response_info = {
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status_code": response.status_code,
                "process_time_seconds": round(process_time, 4),
            }

            # Log response body for certain status codes and if enabled
            if self.log_body and hasattr(response, 'body'):
                try:
                    if isinstance(response, StreamingResponse):
                        response_info["body"] = "<Streaming Response>"
                    elif response.status_code >= 400:  # Always log error responses
                        body = response.body
                        if body and len(body) <= self.max_body_size:
                            try:
                                response_info["body"] = json.loads(body.decode())
                            except (json.JSONDecodeError, UnicodeDecodeError):
                                response_info["body"] = body.decode('utf-8', errors='ignore')
                        elif len(body) > self.max_body_size:
                            response_info["body"] = f"<Body too large: {len(body)} bytes>"
                except Exception as e:
                    response_info["body_error"] = f"Could not read response body: {str(e)}"

            # Determine log level based on status code
            if response.status_code >= 500:
                logger.error(f"OUTGOING RESPONSE: {json.dumps(response_info, indent=2)}")
            elif response.status_code >= 400:
                logger.warning(f"OUTGOING RESPONSE: {json.dumps(response_info, indent=2)}")
            else:
                logger.info(f"OUTGOING RESPONSE: {json.dumps(response_info, indent=2)}")

        except Exception as e:
            logger.error(f"Error logging response {request_id}: {str(e)}")

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request"""
        # Check for forwarded headers (common in reverse proxy setups like Render)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        return request.client.host if request.client else "unknown"


class PerformanceLoggingMiddleware(BaseHTTPMiddleware):
    """
    Separate middleware for performance monitoring
    """

    def __init__(self, app, slow_request_threshold: float = 1.0):
        """
        Initialize performance middleware

        Args:
            app: FastAPI application
            slow_request_threshold: Time in seconds to consider a request slow
        """
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log slow requests
        if process_time > self.slow_request_threshold:
            logger.warning(
                f"SLOW REQUEST: {request.method} {request.url.path} "
                f"took {process_time:.4f}s (threshold: {self.slow_request_threshold}s)"
            )

        # Add processing time header
        response.headers["X-Process-Time"] = str(round(process_time, 4))

        return response