from .api.app import criar_app
from .di.provedores import montar_container

app = criar_app(montar_container())
