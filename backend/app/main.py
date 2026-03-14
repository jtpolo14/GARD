from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import agents, decisions, decision_logs, health, policies, processes, rules, simulations
from app.seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(agents.router, prefix="/api/v1")
app.include_router(processes.router, prefix="/api/v1")
app.include_router(rules.router, prefix="/api/v1")
app.include_router(policies.router, prefix="/api/v1")
app.include_router(decisions.router, prefix="/api/v1")
app.include_router(decision_logs.router, prefix="/api/v1")
app.include_router(simulations.router, prefix="/api/v1")
