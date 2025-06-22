class Container:
    """Minimal dependency injection container."""

    def __init__(self):
        self._providers = {}

    def register(self, name: str, provider):
        self._providers[name] = provider

    def get(self, name: str):
        provider = self._providers[name]
        return provider() if callable(provider) else provider
