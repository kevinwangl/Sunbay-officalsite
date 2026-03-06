from ..dingtalk import SheetManager, DingTalkConfig, SheetError
from ..models.contact import ContactForm
from typing import Dict


class ContactService:
    """联系人业务服务"""
    
    def __init__(self, config: DingTalkConfig, sheet_id: str, table_id: str = "tbl001"):
        self.sheet = SheetManager(config)
        self.sheet_id = sheet_id
        self.table_id = table_id
    
    def save_contact(self, contact: ContactForm, client_ip: str = "") -> Dict:
        """保存联系信息到钉钉表格"""
        try:
            data = {
                "name": contact.name,
                "phone": contact.phone,
                "email": contact.email,
                "company": contact.company or "",
                "message": contact.message or "",
                "ip": client_ip,
            }
            return self.sheet.add_record(self.sheet_id, data, self.table_id)
        except SheetError:
            raise

    def check_duplicate(self, phone: str = None, email: str = None) -> bool:
        """检查手机号或邮箱是否已提交过"""
        try:
            records = self.sheet.get_records(
                self.sheet_id, self.table_id, fields=["手机", "邮箱"]
            )
            for record in records:
                if phone and record.get("手机") == phone:
                    return True
                if email and record.get("邮箱") == email:
                    return True
            return False
        except SheetError:
            return False  # 查询失败不阻断提交
