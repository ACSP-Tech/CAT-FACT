#importing the necessary requirements
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database_setup import init_db
from .setup_main import configure_cors, configure_logging_middleware

#importing router
from .routers import cat_fact, add_user, root, keep_alive

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

#calling an instance of fast api
app = FastAPI(
    title="E-Library API",
    description="Random Cat Fact Application",
    version="1.0.0",
    lifespan=lifespan
)

#defining the cors function and any other custom middleware
configure_cors(app)

# CONFIGURE LOGGING MIDDLEWARE
configure_logging_middleware(app)

#adding router to FastAPI application
app.include_router(cat_fact.router)
app.include_router(add_user.router)
app.include_router(root.router)
app.include_router(keep_alive.router)