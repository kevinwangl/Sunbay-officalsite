from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    DINGTALK_APP_KEY: str
    DINGTALK_APP_SECRET: str
    DINGTALK_CORP_ID: str = "dingfa771f64e3b6b29ea1320dcb25e91351"  # 企业ID
    DINGTALK_SHEET_ID: str
    DINGTALK_TABLE_ID: str = "tbl001"
    DINGTALK_OPERATOR_ID: str = "system"  # 操作者ID，默认使用system
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 10000
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR
    
    class Config:
        env_file = ".env"


settings = Settings()
