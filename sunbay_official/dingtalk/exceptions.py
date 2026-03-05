class DingTalkError(Exception):
    """钉钉API基础异常"""
    pass


class AuthError(DingTalkError):
    """认证异常"""
    pass


class SheetError(DingTalkError):
    """表格操作异常"""
    pass
