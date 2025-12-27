from src.template_registry import TemplateRegistry, get_default_registry, get_template


def test_registry_singleton():
    """Prüft, ob der globale Registry-Zugriff korrekt funktioniert."""
    registry = get_default_registry()
    assert isinstance(registry, TemplateRegistry)
    available = registry.list_available()
    assert "taupunkt" in available
    assert "taupunkt_advanced" in available


def test_get_template_instance():
    """Prüft, ob die Registry korrekte Instanzen liefert."""
    template = get_template("taupunkt")
    assert template is not None
    # Prüft auf den Namen aus der Taupunkt-Klasse
    assert "Taupunkt" in template.get_name()


def test_get_template_info():
    """Prüft, ob die vollständigen Informationen (Struktur/Meta) geliefert werden."""
    registry = get_default_registry()
    info = registry.get_template_info("taupunkt")
    assert info is not None
    assert info["id"] == "taupunkt"
    assert "structure" in info
    assert "metadata" in info


def test_registry_list_available():
    """Prüft, ob die Liste der verfügbaren Templates korrekt ist."""
    registry = get_default_registry()
    available = registry.list_available()
    assert isinstance(available, list)
    assert "taupunkt" in available
    assert "taupunkt_advanced" in available
