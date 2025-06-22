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

## Dependency Management

Produktive Abhängigkeiten werden in `requirements.txt` gepflegt, Entwicklungswerkzeuge in `requirements-dev.txt`. Mit `pip-compile` aus dem Paket `pip-tools` lassen sich daraus Lock-Files erstellen.

## Neues Projekt erzeugen

Ein neues Projektgerüst kann mit dem CLI-Modul `generate_project` erstellt werden:

```bash
python -m src.generate_project my_project
```

Die dafür genutzte `VirtualEnvironmentManager`-Klasse legt automatisch ein
`.venv`-Verzeichnis an und installiert auf Wunsch Abhängigkeiten.
Zusätzlich erzeugt `VSCodeIntegration` passende Einstellungen und Tasks im
`.vscode`-Ordner, damit der Interpreter direkt erkannt wird.
