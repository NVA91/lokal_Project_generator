# project_generator

kleiner Helfer ;)

# Mein Projekt

Dieses Projekt enthält die Hauptanwendung, Tests und Dokumentation.

## Struktur

* src/: Quellcode
* tests/: Unit-Tests
* docs/: Dokumentation

## Nutzung

Das Hauptprogramm befindet sich in `src/project_generator/main.py`. Starte es mit einem optionalen Zielpfad:

```bash
python -m project_generator.main path/to/project
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
