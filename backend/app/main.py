import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from casbin import CasbinMiddleware, CasbinConfig

from app.common.database import engine
from app.common.database import SQLModel
from app.config.config import settings
from app.middleware.logging import LogRequestsMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.module.auth import routers as auth_routers
from app.module.client import routers as client_routers
from app.module.client import models as client_models
from app.module.message import routers as message_routers
from app.module.message import models as message_models
from app.module.payment import routers as payment_routers
from app.module.payment import models as payment_models
from app.module.task import routers as task_routers
from app.module.task import models as task_models
from app.module.task_rating import routers as task_rating_routers
from app.module.task_rating import models as task_rating_models
from app.module.task_worker import routers as task_worker_routers
from app.module.task_worker import models as task_worker_models
from app.module.user import routers as user_routers
from app.module.user import models as user_models
from app.module.worker import routers as worker_routers
from app.module.worker import models as worker_models

description = """
Human Worker is a marketplace where AIs pay humans to work

Humans can sign up to get paid for tasks that AIs need help on.

AIs can sign up and create tasks for humans to help them with.
"""

app = FastAPI(
    title="Human Worker",
    description=description,
    summary="Human Worker is a marketplace where AIs pay humans to work",
    version="0.0.1",
    terms_of_service="{config.hostname}/terms/",
    contact={
        "name": "Jacob Valdez",
        "url": "{config.hostname}/contact/",
        "email": "jacob@humanworker.ai",
    },
    license_info={
        "name": "Proprietary",
        "url": "{config.hostname}/license/",
    },
)

# Create all database tables
SQLModel.metadata.create_all(engine)

# Add Casbin middleware
casbin_conf = CasbinConfig(
    model_path="app/config/casbin/model.conf",
    policy_path="app/config/casbin/policy.csv",
)
app.add_middleware(CasbinMiddleware, config=casbin_conf)

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for Trusted Hosts
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]
)

# Middleware for Logging Requests
app.add_middleware(LogRequestsMiddleware)

# Middleware for Security Headers
app.add_middleware(SecurityHeadersMiddleware)

# Include routers
app.include_router(user_routers.router, prefix="/users", tags=["users"])
app.include_router(client_routers.router, prefix="/clients", tags=["clients"])
app.include_router(worker_routers.router, prefix="/workers", tags=["workers"])
app.include_router(task_routers.router, prefix="/tasks", tags=["tasks"])
app.include_router(
    task_worker_routers.router, prefix="/task_workers", tags=["task_workers"]
)
app.include_router(message_routers.router, prefix="/messages", tags=["messages"])
app.include_router(payment_routers.router, prefix="/payments", tags=["payments"])
app.include_router(
    task_rating_routers.router, prefix="/task_ratings", tags=["task_ratings"]
)
app.include_router(auth_routers.router, prefix="/auth", tags=["auth"])

# Authentication and token routes
# import directly above use to minimize attack surface
from app.module.auth import routers as auth_router

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
