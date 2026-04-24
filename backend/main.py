import torch
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routes import api

torch.set_float32_matmul_precision('medium')


settings = get_settings()

app = FastAPI(
    title="Yansu — Inspeção Óptica Inteligente",
    description="API de detecção de anomalias em PCBs usando Aprendizado Não Supervisionado.",
    version="2.4.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)


@app.get("/health", tags=["infra"])
async def health() -> dict:
    return {"status": "ok", "version": "2.4.1"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
