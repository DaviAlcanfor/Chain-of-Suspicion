from pydantic import BaseModel, Field

from .api_keys import APIKeySettings
from .jogo import GameSettings
from .llm import LLMSettings


class Settings(BaseModel):
    api_keys: APIKeySettings = Field(default_factory=APIKeySettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    game: GameSettings = Field(default_factory=GameSettings)


settings = Settings()
