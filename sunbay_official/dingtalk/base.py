"""
钉钉API基础客户端
提供通用的认证和配置管理
"""
from typing import Optional
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.oauth2_1_0 import client as oauth_client, models as oauth_models
from .exceptions import AuthError
from ..logger import logger


class DingTalkConfig:
    """钉钉配置"""
    
    def __init__(
        self,
        app_key: str,
        app_secret: str,
        corp_id: str,
        operator_id: Optional[str] = None
    ):
        self.app_key = app_key
        self.app_secret = app_secret
        self.corp_id = corp_id
        self.operator_id = operator_id
    
    @classmethod
    def from_settings(cls, settings):
        """从Settings对象创建配置"""
        return cls(
            app_key=settings.DINGTALK_APP_KEY,
            app_secret=settings.DINGTALK_APP_SECRET,
            corp_id=settings.DINGTALK_CORP_ID,
            operator_id=settings.DINGTALK_OPERATOR_ID
        )


class DingTalkBaseClient:
    """钉钉API基础客户端"""
    
    def __init__(self, config: DingTalkConfig):
        self.config = config
        self._oauth_client = self._create_oauth_client()
        self._access_token_cache = None
    
    def _create_oauth_client(self) -> oauth_client.Client:
        """创建OAuth客户端"""
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return oauth_client.Client(config)
    
    def _create_api_config(self) -> open_api_models.Config:
        """创建API客户端配置"""
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return config
    
    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        获取access_token
        
        Args:
            force_refresh: 是否强制刷新token
            
        Returns:
            access_token字符串
            
        Raises:
            AuthError: 认证失败时抛出
        """
        if self._access_token_cache and not force_refresh:
            return self._access_token_cache
        
        logger.info("获取钉钉 access_token")
        
        try:
            request = oauth_models.GetTokenRequest(
                grant_type='client_credentials',
                client_id=self.config.app_key,
                client_secret=self.config.app_secret
            )
            response = self._oauth_client.get_token(self.config.corp_id, request)
            
            if response and response.body and response.body.access_token:
                self._access_token_cache = response.body.access_token
                logger.info("access_token 获取成功")
                return self._access_token_cache
            
            logger.error("access_token 响应为空")
            self._access_token_cache = None
            raise AuthError("获取access_token失败：响应为空")
            
        except Exception as e:
            logger.error(f"认证失败 | error={str(e)}")
            self._access_token_cache = None
            raise AuthError(f"认证失败: {str(e)}")
    
    def create_headers(self, header_class, include_operator_id: bool = False):
        """
        创建API请求头
        
        Args:
            header_class: 钉钉SDK的Headers类
            include_operator_id: 是否包含operatorId
            
        Returns:
            配置好的headers对象
        """
        headers = header_class()
        headers.x_acs_dingtalk_access_token = self.get_access_token()
        
        if include_operator_id and self.config.operator_id:
            headers.common_headers = {
                "operatorId": self.config.operator_id,
                "x-acs-dingtalk-operator-id": self.config.operator_id,
                "operator-id": self.config.operator_id
            }
        
        return headers
