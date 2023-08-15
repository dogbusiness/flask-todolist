import os

from pydantic import Field
from pydantic_settings import BaseSettings

basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    app_secret_key: str = Field(
        default="h)8@p^44j1c_(5!w)%&u!-#i+3d_f=5*g@4s_zhb30^", env="SECRET_KEY"
    )
    database_uri: str = Field(
        default="sqlite:///" + os.path.join(basedir, "app.db"),
        env="DATABASE_URI",  # noqa: E501
    )


settings = Settings()
