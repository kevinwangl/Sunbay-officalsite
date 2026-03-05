from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ContactForm(BaseModel):
    """联系表单模型"""
    name: str = Field(..., min_length=1, max_length=50, description="姓名")
    email: EmailStr = Field(..., description="邮箱")
    company: str = Field(..., min_length=1, max_length=100, description="公司")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    message: Optional[str] = Field(None, max_length=500, description="留言")
