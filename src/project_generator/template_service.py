class TemplateService:
    """Very small template renderer using str.format."""

    def render(self, template: str, context: dict) -> str:
        return template.format(**context)
