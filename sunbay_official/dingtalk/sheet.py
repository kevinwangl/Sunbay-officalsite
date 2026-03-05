from typing import Dict, Any
from alibabacloud_dingtalk.notable_1_0 import client, models
from alibabacloud_tea_util import models as util_models
from .base import DingTalkBaseClient, DingTalkConfig
from .exceptions import SheetError, AuthError


class SheetManager(DingTalkBaseClient):
    """钉钉智能表格管理器"""
    
    def __init__(self, config: DingTalkConfig):
        super().__init__(config)
        self._client = self._create_notable_client()
    
    def _create_notable_client(self):
        return client.Client(self._create_api_config())
    
    def add_record(self, sheet_id: str, data: Dict[str, Any], table_id: str = "tbl001") -> Dict:
        """添加记录到智能表格"""
        try:
            if not self.config.operator_id:
                raise SheetError("未配置DINGTALK_OPERATOR_ID")
            
            record_fields = {
                "姓名": data.get("name", ""),
                "手机": data.get("phone", ""),
                "邮箱": data.get("email", ""),
                "公司": data.get("company", ""),
                "留言": data.get("message", "")
            }
            
            record = models.InsertRecordsRequestRecords(fields=record_fields)
            # notable_1_0 的 operator_id 在 request body 中
            request = models.InsertRecordsRequest(
                records=[record],
                operator_id=self.config.operator_id
            )
            
            headers = models.InsertRecordsHeaders()
            headers.x_acs_dingtalk_access_token = self.get_access_token()
            
            response = self._client.insert_records_with_options(
                sheet_id, table_id, request, headers, util_models.RuntimeOptions()
            )
            
            if response and response.body and response.body.value:
                return {"success": True, "record_id": response.body.value[0]}
            
            raise SheetError("响应数据为空")
            
        except AuthError:
            raise
        except Exception as e:
            raise SheetError(f"添加记录失败: {str(e)}")

    def get_records(self, sheet_id: str, table_id: str, fields: list = None) -> list:
        """查询表格记录"""
        try:
            request = models.GetRecordsRequest(
                max_results=100,
                operator_id=self.config.operator_id
            )

            headers = models.GetRecordsHeaders()
            headers.x_acs_dingtalk_access_token = self.get_access_token()

            response = self._client.get_records_with_options(
                sheet_id, table_id, request, headers, util_models.RuntimeOptions()
            )

            if response and response.body:
                records = response.body.to_map().get('records', [])
                if fields:
                    return [
                        {f: r.get('fields', {}).get(f) for f in fields}
                        for r in records
                    ]
                return [r.get('fields', {}) for r in records]

            return []

        except AuthError:
            raise
        except Exception as e:
            raise SheetError(f"查询记录失败: {str(e)}")
