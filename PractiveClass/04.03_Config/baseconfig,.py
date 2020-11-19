import os
import pydantic
from pydantic_choices import choice

basedir = os.path.abspath(os.path.dirname(__file__))

LogLevel = choice(["DEBUG", "INFO", "WARNING", "CRITICAL"])


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_prefix = ""
        env_file = "regist_sshpubkey.env"
        env_file_encoding = "utf-8"
        use_enum_values = True

