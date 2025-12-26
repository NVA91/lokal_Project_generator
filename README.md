# project_generator

kleiner Helfer ;)

# Mein Projekt

Dieses Projekt enthält die Hauptanwendung, Tests und Dokumentation.

## Struktur

* src/: Quellcode
* tests/: Unit-Tests
* docs/: Dokumentation

## Nutzung

Das Hauptprogramm befindet sich in `src/main.py`. Starte es mit:

```bash
python -m src.main
```

## Entwicklungs-Setup

Führe das Skript `setup_project.sh` aus, um die Verzeichnisstruktur anzulegen und ein virtuelles Environment zu erstellen:

```bash
./setup_project.sh
```

Tests können mit folgendem Skript ausgeführt werden:

```bash
./run_tests.sh
```


## GUI-Preview

Neben dem simplen CLI-Einstieg steht eine kleine Tkinter-GUI zur Verfügung. Sie wird mit folgendem Befehl gestartet:

```bash
python -m src.gui
```

Die Anwendung zeigt eine Baumansicht der verfügbaren Templates und bietet eine Fortschrittsanzeige während der Projekterstellung.
Templates können über die Combobox ausgewählt werden. Neue Vorlagen lassen sich über den "Import"-Button oder per Drag‑&‑Drop hinzufügen. Beim Generieren wird der Kopiervorgang in einem Hintergrund-Thread ausgeführt, sodass die Oberfläche responsiv bleibt.
Die GUI nutzt das moderne ``clam``-Theme von ttk und passt sich dank Grid-Layout dynamisch an die Fenstergröße an.

## Dependency-Management

Im Reiter ``Dependencies`` kann ein virtuelles Environment eingerichtet werden.
Wähle eine Python-Version und optional vorkonfigurierte Paket-Sets aus.
Der Fortschritt des Setups wird über eine zusätzliche Leiste angezeigt.

## Spezialisierte Templates

Das Paket bringt einige vordefinierte Templates mit, die alle die Klasse
``TemplateBase`` implementieren. Sie liefern vollständige Verzeichnisstrukturen
inklusive Metadaten:

- **SmartHomeTemplate** – Vorlage für LED-Controller-Projekte mit Hardware-Doku
  und ``wled_config.json``.
- **AutomationTemplate** – enthält Beispiel-Workflows für CI/CD und
  Automatisierungsskripte.
- **GameDevTemplate** – Basis für ein Flutter-Kartenspiel samt Assets und
  ``pubspec.yaml``.
