# Quickstart: Taupunkt Template nutzen

## 🚀 Direkt loslegen

### 1. Umgebung aktivieren

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ 
```

Wenn dein venv nicht aktiv ist:

```bash
source .venv/bin/activate
```

### 2. Dependencies installieren

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ pip install -e .
```

### 3. Taupunkt Template erkunden

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ python examples/taupunkt_example.py
```

**Output:**
```
============================================================
Taupunkt Template Examples
============================================================

=== Available Templates ===

  Taupunkt - Dew Point Display
    ID: taupunkt
    Description: MicroPython-based environmental monitoring...

  Taupunkt Advanced - Cloud Connected
    ID: taupunkt_advanced
    Description: Advanced MicroPython project with cloud...

=== Taupunkt Template Structure ===
[folder structure displayed]

=== Taupunkt Metadata ===
Framework: MicroPython
Platform: Raspberry Pi Pico 2
Language: Python 3

Dependencies:
  - MicroPython
  - micropython-st7789
  - micropython-aht20
  - micropython-bmp280
  - micropython-sht41

[... mehr Details ...]
```

## 📝 Interaktive Nutzung

### Python REPL starten

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ python
```

### Templates auflisten

```python
>>> from src.template_registry import list_templates, get_template_info
>>>
>>> for tmpl in list_templates():
...     info = get_template_info(tmpl)
...     print(f"{info['name']} ({tmpl})")
...
Taupunkt - Dew Point Display (taupunkt)
Taupunkt Advanced - Cloud Connected (taupunkt_advanced)
```

### Taupunkt Details abrufen

```python
>>> from src.template_registry import get_template_info
>>>
>>> info = get_template_info("taupunkt")
>>>
>>> print(info['description'])
MicroPython-based environmental monitoring and dew point display...
>>>
>>> print("\nHardware:")
Hardware:
>>> for key, val in info['metadata']['controller_specs'].items():
...     print(f"  {key}: {val}")
...
  model: Raspberry Pi Pico 2
  processor: ARM Cortex-M33
  frequency: 150 MHz
  ram: 520 KB
  flash: 4 MB
  gpio_pins: 26
  interfaces: ['SPI', 'I2C', 'UART']
```

### Sensoren ansehen

```python
>>> sensors = info['metadata']['dew_point_sensors']
>>>
>>> for sensor in sensors:
...     print(f"\n{sensor['name']} @ 0x{sensor['address']}")
...     print(f"  Type: {sensor['type']}")
...

SHT41 @ 0x44
  Type: Indoor humidity/temperature

AHT20 @ 0x38
  Type: Ambient humidity/temperature

BMP280 @ 0x76
  Type: Barometric pressure
```

### Projektstruktur inspizieren

```python
>>> from src.template_registry import get_template
>>>
>>> template = get_template("taupunkt")
>>> structure = template.get_structure()
>>>
>>> # Toplevel zeigen
>>> for item in structure.keys():
...     print(item)
...
src
micropython
docs
config
tests
examples
README.md
.gitignore
```

### Projekt generieren

```python
>>> from pathlib import Path
>>> from src.template_registry import get_template
>>>
>>> template = get_template("taupunkt")
>>> structure = template.get_structure()
>>> project_dir = Path("/tmp/my_taupunkt_project")
>>>
>>> # Rekursiv Ordner & Dateien erstellen
>>> def create_structure(base, struct):
...     base.mkdir(parents=True, exist_ok=True)
...     for name, content in struct.items():
...         path = base / name
...         if isinstance(content, dict):
...             create_structure(path, content)
...         else:  # Datei
...             path.touch()
...
>>> create_structure(project_dir, structure)
>>> print(f"✅ Project created at {project_dir}")
✅ Project created at /tmp/my_taupunkt_project
```

Verifizieren:

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ ls -la /tmp/my_taupunkt_project/
```

## 🛠️ Template in der GUI verwenden

### GUI starten

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ python -m src.gui
```

oder mit app.py:

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ python src/gui.py
```

## 📚 Detaillierte Dokumentation

```bash
# Registry System
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ less TEMPLATE_REGISTRY.md

# Taupunkt spezifisch
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ less docs/TAUPUNKT_TEMPLATE.md

# Changelog
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ less NEWS.md
```

## 🔍 Häufige Aufgaben

### Template-Liste mit Beschreibungen

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ python -c "
from src.template_registry import get_default_registry
reg = get_default_registry()
for name, desc in reg.list_with_descriptions().items():
    print(f'\n{name}:')
    print(f'  {desc}')
"
```

### Template komplette Info als JSON

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ python -c "
import json
from src.template_registry import get_template_info
info = get_template_info('taupunkt')
print(json.dumps(info, indent=2))
" | head -50
```

### Nur Dependencies anzeigen

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ python -c "
from src.template_registry import get_template_info
info = get_template_info('taupunkt')
for dep in info['metadata'].get('dependencies', []):
    print(f'  - {dep}')
"
```

### Pin-Konfiguration

```bash
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ python -c "
from src.template_registry import get_template_info
import json
info = get_template_info('taupunkt')
pins = info['metadata'].get('pin_configuration', {})
print(json.dumps(pins, indent=2))
"
```

## 🐛 Troubleshooting

### ModuleNotFoundError

```bash
# Package installieren
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ pip install -e .
```

### Import-Fehler

```bash
# Sicherstellen, dass venv aktiv ist
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ which python
/workspaces/lokal_Project_generator/.venv/bin/python
```

### Beispiel-Skript funktioniert nicht

```bash
# Direkter Pfad nutzen
(.venv) @NVA91 ➜ /workspaces/lokal_Project_generator (main) $ python ./examples/taupunkt_example.py
```

## 🎯 Nächste Schritte

1. **Template erkunden** → `python examples/taupunkt_example.py`
2. **Projekt erstellen** → Struktur generieren mit Python
3. **Konfigurieren** → `config/default_config.json` anpassen
4. **Entwickeln** → Sensoren & Display implementieren
5. **Testen** → MicroPython auf Pico 2 testen

## 📦 Struktur nach Projekt-Generierung

```
my_taupunkt_project/
├── src/                    # Python Development Code
│   ├── sensors/           # Sensor drivers
│   ├── display/           # Display driver & UI
│   └── utils/             # Utilities (dew point calc etc)
├── micropython/           # Code für Pico 2 (MicroPython)
│   ├── lib/              # Libraries
│   ├── boot.py           # Device boot
│   └── main.py           # Device main
├── config/               # Konfigurationsdateien
│   ├── default_config.json
│   └── sensor_offsets.json
├── docs/                 # Dokumentation
├── tests/                # Unit tests
├── examples/             # Anwendungsbeispiele
└── README.md
```

## 💡 Pro-Tipps

### Varianten vergleichen

```python
from src.template_registry import get_template_info

basic = get_template_info('taupunkt')
advanced = get_template_info('taupunkt_advanced')

print("Basic Features:", len(basic['metadata']['features']))
print("Advanced Features:", len(advanced['metadata']['features']))
```

### Eigenes Template hinzufügen

Siehe `TEMPLATE_REGISTRY.md` → "Adding New Templates"

### Shell-Alias für schnelle Nutzung

```bash
alias list-templates='python -c "from src.template_registry import list_templates; [print(t) for t in list_templates()]"'
alias show-taupunkt='python examples/taupunkt_example.py'
```

---

**Viel Spaß mit Taupunkt! 🎉**

Fragen? → Siehe `docs/TAUPUNKT_TEMPLATE.md` oder `TEMPLATE_REGISTRY.md`
