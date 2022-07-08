from baseconfig import basedir, BaseSettings, LogLevel
from typing import Optional

class MAILSettings(BaseSettings):
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USE_SSL: bool = False
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_DEFAULT_SENDER: Optional[str] = "iisaka51@gmail.com"
    # for debug
    MAIL_DEBUG: bool = False
    MAIL_SUPPRESS_SEND: bool = False


