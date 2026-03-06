from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .api import contact
from .config import settings
from .logger import logger
import os

app = FastAPI(title="Sunbay Official Website", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(contact.router)


@app.get("/health")
async def health():
    return {"status": "ok"}


def run():
    logger.info(f"启动 Sunbay 服务 | host={settings.SERVER_HOST} | port={settings.SERVER_PORT}")
    logger.info(f"配置加载 | sheet_id={settings.DINGTALK_SHEET_ID} | table_id={settings.DINGTALK_TABLE_ID}")
    
    import uvicorn
    uvicorn.run(
        "sunbay_official.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )


if __name__ == "__main__":
    run()
