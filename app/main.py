#importing the necessary requirements
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database_setup import init_db
from .setup_main import configure_cors, register_exception_handlers
from .middleware import LoggingMiddleware

#importing router
from .routers import cat_fact, add_user, root, keep_alive, string_analysis

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

#calling an instance of fast api
app = FastAPI(
    title="CAT FACT API",
    description="Random Cat Fact Application",
    version="1.0.0",
    lifespan=lifespan
)

#defining the cors function and any other custom middleware
configure_cors(app)

#handling validation error
register_exception_handlers(app)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

#adding router to FastAPI application
app.include_router(cat_fact.router)
app.include_router(add_user.router)
app.include_router(root.router)
app.include_router(keep_alive.router)
app.include_router(string_analysis.router)