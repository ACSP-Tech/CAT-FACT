from fastapi.middleware.cors import CORSMiddleware
from .middleware import RequestResponseLoggingMiddleware, PerformanceLoggingMiddleware

def configure_cors(app):
    """Configure CORS middleware for the FastAPI app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def configure_logging_middleware(app):
    """Configure logging middleware for the FastAPI app."""

    # Add performance monitoring middleware
    app.add_middleware(
        PerformanceLoggingMiddleware,
        slow_request_threshold=2.0  # Log requests taking more than 2 seconds
    )

    # Add request/response logging middleware
    app.add_middleware(
        RequestResponseLoggingMiddleware,
        log_body=False,  # Set to False to avoid logging request/response bodies
        max_body_size=2048  # Maximum body size to log (2KB)
    )