from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from ..models.contact import ContactForm
from ..services.contact_service import ContactService
from ..dingtalk import DingTalkConfig
from ..config import settings

router = APIRouter(prefix="/api", tags=["contact"])

dingtalk_config = DingTalkConfig.from_settings(settings)
contact_service = ContactService(
    config=dingtalk_config,
    sheet_id=settings.DINGTALK_SHEET_ID,
    table_id=settings.DINGTALK_TABLE_ID
)


@router.post("/contact", status_code=status.HTTP_201_CREATED)
async def submit_contact(contact: ContactForm):
    """提交联系表单"""
    try:
        result = contact_service.save_contact(contact)
        return {"success": True, "message": "提交成功", "data": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"提交失败: {str(e)}"
        )


@router.get("/contact/check")
async def check_duplicate(
    phone: Optional[str] = Query(None, description="手机号"),
    email: Optional[str] = Query(None, description="邮箱")
):
    """检查手机号或邮箱是否已提交过"""
    if not phone and not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请提供 phone 或 email 参数"
        )
    
    is_duplicate = contact_service.check_duplicate(phone=phone, email=email)
    return {"duplicate": is_duplicate}
