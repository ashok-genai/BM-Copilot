
from fastapi import FastAPI
from app.core.config import settings
from app.api.health import router as health_router
from app.api.customers import router as customer_router
from app.api.assistant import router as assistant_router

app = FastAPI(
    title=settings.app_name,
    description="AI-Powered ERP and Manufacturing Assistant",
    version="1.0.0"
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"]
)

app.include_router(
    customer_router,
    prefix="/api/v1/customers",
    tags=["Customers"]
)

@app.get("/")
def home():
    return {
        "message": "Welcome to BM Copilot",
        "description": "AI-Powered ERP Assistant",
        "status": "running"
    }

# AI Assistant API
app.include_router(
    assistant_router,
    prefix="/api/v1/assistant",
    tags=["AI Assistant"]
)