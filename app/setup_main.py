from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def configure_cors(app):
    """Configure CORS middleware for the FastAPI app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True
)

logger = logging.getLogger(__name__)



# Define the handler function
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler to differentiate between:
    - 400: Missing 'value' field
    - 422: Invalid type or invalid content
    """
    errors = exc.errors()
    
    for error in errors:
        #check if query parameter is missing
        if "query" in error["loc"]:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid query parameter values or types"}
            )
        # Check if entire request body is missing
        if error['loc'] == ('body',) and error['type'] == 'missing':
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Invalid request body or missing 'value' field"}
            )
        
        # Check if 'value' field is in the error location
        if 'value' in error['loc']:
            
            # Missing field → 400
            if error['type'] == 'missing':
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "Invalid request body or missing 'value' field"}
                )
            
            # Wrong type → 422
            if error['type'] in ['string_type', 'string_unicode']:
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content={"detail": "Invalid data type for 'value' (must be string)"}
                )
            
            # Other validation errors → 422
            if error['type'] == 'value_error':
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content={"detail": error['msg']}
                )
    
    # Default fallback
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors}
    )


# Registration function
def register_exception_handlers(app: FastAPI):
    """Register all custom exception handlers"""
    app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)