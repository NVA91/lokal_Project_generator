from src.taupunkt_template import TaupunktTemplate, TaupunktAdvancedTemplate


def test_taupunkt_base_metadata():
    """Prüft die Hardware-Spezifikationen des Taupunkt-Templates."""
    t = TaupunktTemplate()
    meta = t.get_metadata()
    # Verifiziert die Plattform und Sensoren
    assert meta["platform"] == "Raspberry Pi Pico 2"
    assert "micropython-sht41" in meta["dependencies"]
    assert "SHT41 (Indoor)" in meta["sensors"].values()


def test_taupunkt_structure():
    """Prüft, ob die MicroPython-spezifischen Ordner vorhanden sind."""
    t = TaupunktTemplate()
    struct = t.get_structure()
    # Prüft die wichtigsten Dateien für den Pico
    assert "micropython" in struct
    assert "boot.py" in struct["micropython"]
    assert "sht41.py" in struct["src"]["sensors"]


def test_taupunkt_advanced_features():
    """Prüft die erweiterten Cloud-Features der Advanced-Version."""
    t = TaupunktAdvancedTemplate()
    struct = t.get_structure()
    meta = t.get_metadata()
    # Prüft die neue Ordnerstruktur für Konnektivität
    assert "connectivity" in struct["src"]
    # Prüft die Cloud-Features in den Metadaten
    assert "MQTT connectivity" in meta["features"]
    assert "Cloud data sync" in meta["features"]
