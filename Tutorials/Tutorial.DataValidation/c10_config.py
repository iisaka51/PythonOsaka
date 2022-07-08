import pydantic
from typing import Optional, Union, List

class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_prefix = ''
        use_enum_values = True

class MAILSettings(BaseSettings):
    MAIL_SERVER: str = 'smtp.gmail.com'
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USE_SSL: bool = False
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_DEFAULT_SENDER: Optional[str] = '_YOU_GMAIL_ADDRESS_HERE_'
    # for debug
    MAIL_DEBUG: bool = False
    MAIL_SUPPRESS_SEND: bool = False
