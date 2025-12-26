# ESP32 Sensor Template System

Komprehensives Template-System für professionelle ESP32 IoT und Sensor-Projekte mit integrierter MQTT-Unterstützung, Hardware-Dokumentation und Konfigurationsverwaltung.

## Überblick

Das ESP32 Template System bietet spezialisierte Projekt-Templates für verschiedene Sensor- und IoT-Anwendungen:

- **Basis-Template**: Generisches ESP32 Sensor-Projekt
- **SHT41 Template**: Temperatur & Luftfeuchte-Überwachung
- **BME680 Template**: Umfassende Luftqualitäts-Überwachung
- **Motion Template**: Bewegungserkennung & Präsenz-Tracking
- **Light Template**: Lichtstärken-Überwachung & Automationen

## Template-Klassen

### ESP32SensorTemplate (Basis)

Basis-Klasse für alle ESP32 Sensor-Projekte. Erlaubt flexible Konfiguration von Sensor-Typ und Kommunikationsprotokoll.

```python
from src.esp32_templates import ESP32SensorTemplate

# Generisches Template
template = ESP32SensorTemplate()

# Mit benutzerdefinierten Parametern
template = ESP32SensorTemplate(
    sensor_type="temp_humidity",
    protocol="mqtt"  # mqtt, http, ble
)
```

#### Struktur
```
src/
├── main.cpp                    # Hauptprogramm
├── config.h                    # Globale Konfiguration
├── sensors/                    # Sensor-Implementierungen
│   ├── [sensor_type].cpp
│   └── [sensor_type].h
├── communication/              # Kommunikations-Module
│   ├── [protocol].cpp
│   └── [protocol].h
└── utils/                      # Hilfsfunktionen
    ├── calibration.cpp/h
    └── logger.cpp/h

docs/
├── hardware/                   # Hardware-Dokumentation
│   ├── pinout.md
│   ├── wiring_diagram.md
│   └── bom.md
└── software/                   # Software-Dokumentation
    ├── api.md
    └── calibration_guide.md

config/
├── platformio.ini              # PlatformIO Konfiguration
├── mqtt_config.json            # MQTT Einstellungen
└── sensor_config.json          # Sensor-Parameter

tests/
├── test_sensors.cpp
└── test_communication.cpp
```

#### Metadaten

```python
metadata = template.get_metadata()

# Enthält:
# - dependencies: PlatformIO/Arduino Bibliotheken
# - config_files: Konfigurationsdateien
# - framework: Arduino
# - platform: esp32
# - features: Unterstützte Funktionen
# - sensor_type: Sensor-Typ
# - communication_protocol: Kommunikationsprotokoll
```

---

### SHT41TemperatureHumidityTemplate

Spezialisiertes Template für **Sensirion SHT41** Sensor mit professioneller Umgebungsüberwachung.

```python
from src.esp32_templates import SHT41TemperatureHumidityTemplate

template = SHT41TemperatureHumidityTemplate()
print(template.get_name())  # "ESP32 SHT41 Environment Monitor"
```

#### Features
- ✅ Temperatur & Luftfeuchte-Messung
- ✅ Taupunktberechnung
- ✅ I2C-Interface
- ✅ Kalibrierung & Kompensation
- ✅ MQTT Integration
- ✅ Datenlogging

#### Sensor-Spezifikationen
```
Modell:              Sensirion SHT41
Interface:           I2C
Messbereich Temp:    -40 bis +125°C
Messbereich Feuchte: 0 bis 100% RH
Genauigkeit Temp:    ±1.5°C
Genauigkeit Feuchte: ±3% RH
```

#### Zusätzliche Dateien
```
docs/
├── hardware/SHT41_datasheet.md
└── software/dew_point_calculation.md

config/sht41_calibration.json
```

---

### BME680AirQualityTemplate

Umfassende Luftqualitäts-Überwachung mit **Bosch BME680** Sensor.

```python
from src.esp32_templates import BME680AirQualityTemplate

template = BME680AirQualityTemplate()
print(template.get_name())  # "ESP32 BME680 Air Quality Monitor"
```

#### Features
- ✅ Temperatur, Luftfeuchte, Luftdruck
- ✅ VOC (flüchtige organische Stoffe) Messung
- ✅ IAQ (Indoor Air Quality) Index-Berechnung
- ✅ I2C/SPI Interface
- ✅ Erweiterte Kalibrierung
- ✅ Beispiel-Code mit MQTT

#### Sensor-Spezifikationen
```
Modell:           Bosch BME680
Interface:        I2C/SPI
Temp-Bereich:     -40 bis +85°C
Druck-Bereich:    300 bis 1100 hPa
Feuchte-Bereich:  0 bis 100% RH
Gas-Messung:      1 bis 500k Ohm
Messungen:        Temp, Feuchte, Druck, VOC
```

#### Zusätzliche Dateien
```
docs/
├── hardware/BME680_datasheet.md
└── software/iaq_calculation.md

examples/
├── basic_reading.cpp
├── with_calibration.cpp
└── mqtt_publish.cpp
```

---

### MotionSensorTemplate

Bewegungserkennung & Präsenz-Tracking mit dualer Sensor-Validierung.

```python
from src.esp32_templates import MotionSensorTemplate

template = MotionSensorTemplate()
```

#### Features
- ✅ PIR-Bewegungserkennung (HC-SR501)
- ✅ Beschleunigungssensor-Validierung (MPU6050)
- ✅ Dual-Sensor Verifizierung
- ✅ Präsenz-Tracking
- ✅ Bewegungs-Statistiken

#### Sensor-Spezifikationen
```
Primär-Sensor:     PIR HC-SR501
Sekundär-Sensor:   MPU6050 Accelerometer
Interfaces:        GPIO, I2C
Detektionsreich:   ~7 Meter
```

---

### LightSensorTemplate

Lichtstärken-Überwachung mit automatischer Steuerung.

```python
from src.esp32_templates import LightSensorTemplate

template = LightSensorTemplate()
```

#### Features
- ✅ Digitale Lichtstärke-Messung
- ✅ Automatische Helligkeits-Steuerung
- ✅ Lux-basierte Auslöser
- ✅ Niedrigenergiemode
- ✅ I2C Interface

#### Sensor-Spezifikationen
```
Modell:              ROHM BH1750FVI
Interface:           I2C
Messbereich:         1 bis 65535 Lux
Auflösung:           1 Lux
Antwortzeit:         ~16 ms
```

---

## Template-Registry

Alle Templates sind über ein zentrales Registry leicht zugänglich:

```python
from src.esp32_templates import ESP32_TEMPLATES

# Verfügbare Keys:
template_keys = list(ESP32_TEMPLATES.keys())
# ['generic', 'sht41', 'bme680', 'motion', 'light']

# Instantiierung über Registry
Template_Class = ESP32_TEMPLATES['sht41']
template = Template_Class()
```

---

## Verwendungsbeispiele

### Beispiel 1: SHT41 Umgebungsmonitor

```python
from src.esp32_templates import SHT41TemperatureHumidityTemplate

template = SHT41TemperatureHumidityTemplate()

# Projekt-Struktur erhalten
structure = template.get_structure()

# Metadaten mit Abhängigkeiten
metadata = template.get_metadata()
print(f"Dependencies: {metadata['dependencies']}")
# Output: Dependencies: ['esp32', 'Arduino', 'PlatformIO', 
#                        'PubSubClient', 'WiFi', 'SHT41', ...]

# Sensor-Spezifikationen
print(f"Sensor: {metadata['sensor_specs']['model']}")
print(f"Genauigkeit: {metadata['sensor_specs']['accuracy_temp']}")
```

### Beispiel 2: Luftqualitäts-Überwachung

```python
from src.esp32_templates import BME680AirQualityTemplate

template = BME680AirQualityTemplate()

# Mit Beispiel-Code
structure = template.get_structure()
examples = structure['examples']
print(f"Verfügbare Beispiele: {list(examples.keys())}")
# Output: ['basic_reading.cpp', 'with_calibration.cpp', 'mqtt_publish.cpp']

# Features anzeigen
metadata = template.get_metadata()
for feature in metadata['features']:
    print(f"  ✓ {feature}")
```

### Beispiel 3: Benutzerdefiniertes Template

```python
from src.esp32_templates import ESP32SensorTemplate

# Custom Sensor-Typ
template = ESP32SensorTemplate(
    sensor_type="custom_sensor",
    protocol="http"
)

metadata = template.get_metadata()
print(f"Framework: {metadata['framework']}")
print(f"Platform: {metadata['platform']}")
print(f"Protocol: {metadata['communication_protocol']}")
```

---

## Konfigurationsdateien

### platformio.ini
```ini
[env:esp32dev]
platform = espressif32
board = esp32doit-devkit-v1
framework = arduino

lib_deps = 
    PubSubClient
    Sensirion/SHT4x
```

### mqtt_config.json
```json
{
  "broker": "mqtt.example.com",
  "port": 1883,
  "username": "user",
  "password": "pass",
  "topic_base": "home/sensors",
  "reconnect_interval": 10
}
```

### sensor_config.json
```json
{
  "update_interval": 60,
  "calibration_enabled": true,
  "logging_enabled": true,
  "log_level": "INFO"
}
```

---

## Testing

Alle Templates werden durch umfassende Tests validiert:

```bash
pytest tests/test_esp32_templates.py -v
```

Test-Kategorien:
- ✅ Template-Initialisierung
- ✅ Struktur-Generierung
- ✅ Metadaten-Validierung
- ✅ Abhängigkeiten-Auflösung
- ✅ Sensor-Spezifikationen
- ✅ Konsistenz-Checks

---

## Best Practices

### 1. Abhängigkeiten verwalten
```python
metadata = template.get_metadata()
deps = metadata['dependencies']
# Verwende diese für platformio.ini lib_deps
```

### 2. Hardware-Dokumentation
```
docs/hardware/
├── pinout.md       # Pin-Belegung
├── wiring_diagram.md  # Schaltplan
└── bom.md          # Stückliste
```

### 3. Kalibrierung implementieren
```cpp
// src/utils/calibration.cpp
void calibrate_sensor() {
    // Sensor-spezifische Kalibrierungslogik
    // Werte in config/[sensor]_calibration.json speichern
}
```

### 4. Datenlogging
```cpp
// src/utils/logger.cpp
Logger logger("sensor_data.csv");
logger.log(temperature, humidity, pressure);
```

---

## Erweiterung & Customization

### Neues Sensor-Template erstellen

```python
from src.template_base import TemplateBase

class CustomSensorTemplate(TemplateBase):
    def __init__(self):
        self.sensor_type = "custom"
        self.protocol = "mqtt"
    
    def get_name(self) -> str:
        return "Custom Sensor"
    
    def get_description(self) -> str:
        return "Custom sensor project"
    
    def get_structure(self) -> Dict[str, Any]:
        # Projektstruktur definieren
        return { ... }
    
    def get_metadata(self) -> Dict[str, Any]:
        # Abhängigkeiten und Metadaten
        return { ... }
```

Dann zum Registry hinzufügen:
```python
ESP32_TEMPLATES['custom'] = CustomSensorTemplate
```

---

## Fehlerbehebung

### Import-Fehler
```python
# ✅ Korrekt
from src.esp32_templates import SHT41TemperatureHumidityTemplate

# ❌ Falsch
from esp32_templates import SHT41TemperatureHumidityTemplate
```

### Abhängigkeitskonflikt
```bash
# Abhängigkeiten neu installieren
pip install -r requirements.txt
pio lib install
```

---

## Lizenz

Diese Templates sind Teil des lokal_Project_Generator und unter der gleichen Lizenz verfügbar.

## Kontakt & Support

Für Fragen oder Verbesserungsvorschläge:
- GitHub Issues: https://github.com/NVA91/lokal_Project_generator
- Email: Siehe Repository-Kontakt
