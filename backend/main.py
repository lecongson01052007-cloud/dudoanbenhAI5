"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router

app = FastAPI(
    title="SIC Clinical RAG API",
    version="1.0.0",
    description="Trợ lý gợi ý chẩn đoán sơ bộ cho bác sĩ; cần bác sĩ xác nhận.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
