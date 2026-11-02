from pydantic import SecretStr

from .ambiente import Ambiente


class APIKeySettings(Ambiente):
    ai_gateway_api_key: SecretStr = SecretStr("")

    @property
    def configurada(self) -> bool:
        return bool(self.ai_gateway_api_key.get_secret_value())
