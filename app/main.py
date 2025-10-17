#importing the necessary requirements
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database_setup import init_db
from .setup_main import configure_cors

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