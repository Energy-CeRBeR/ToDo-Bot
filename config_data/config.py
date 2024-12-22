from dataclasses import dataclass
from environs import Env

MAX_OBJECTS_ON_PAGE = 10
MAX_NAME_LENGTH = 50
MAX_DESCRIPTION_LENGTH = 500


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        )
    )
