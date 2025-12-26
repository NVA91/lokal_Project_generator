"""ESP32 Sensor and IoT project templates.

This module provides specialized templates for ESP32-based IoT projects
including sensor data acquisition, MQTT integration, and hardware control.
"""

from __future__ import annotations

from typing import Any, Dict
from .template_base import TemplateBase


class ESP32SensorTemplate(TemplateBase):
    """Base template for ESP32 sensor projects with MQTT integration."""

    def __init__(self, sensor_type: str = "generic", protocol: str = "mqtt"):
        """Initialize ESP32 sensor template.

        Args:
            sensor_type: Type of sensor (e.g., 'temp_humidity', 'air_quality')
            protocol: Communication protocol (mqtt, http, ble)
        """
        self.sensor_type = sensor_type
        self.protocol = protocol

    def get_name(self) -> str:
        """Return the template's display name."""
        return f"ESP32 {self.sensor_type.title()} Sensor"

    def get_description(self) -> str:
        """Return a short description of the template."""
        return (
            f"ESP32 IoT sensor project with {self.protocol.upper()} integration. "
            f"Includes sensor calibration, data logging, and cloud sync."
        )

    def get_structure(self) -> Dict[str, Any]:
        """Return the project folder structure."""
        return {
            "src": {
                "main.cpp": None,
                "config.h": None,
                "sensors": {
                    f"{self.sensor_type}.cpp": None,
                    f"{self.sensor_type}.h": None,
                },
                "communication": {
                    f"{self.protocol}.cpp": None,
                    f"{self.protocol}.h": None,
                },
                "utils": {
                    "calibration.cpp": None,
                    "calibration.h": None,
                    "logger.cpp": None,
                    "logger.h": None,
                },
            },
            "include": {},
            "lib": {},
            "docs": {
                "hardware": {
                    "pinout.md": None,
                    "wiring_diagram.md": None,
                    "bom.md": None,
                },
                "software": {
                    "api.md": None,
                    "calibration_guide.md": None,
                },
                "README.md": None,
            },
            "config": {
                "platformio.ini": None,
                "mqtt_config.json": None,
                "sensor_config.json": None,
            },
            "tests": {
                "test_sensors.cpp": None,
                "test_communication.cpp": None,
            },
            "README.md": None,
            ".gitignore": None,
        }

    def get_metadata(self) -> Dict[str, Any]:
        """Return template metadata including dependencies."""
        base_deps = [
            "esp32",
            "Arduino",
            "PlatformIO",
        ]

        protocol_deps = {
            "mqtt": ["PubSubClient", "WiFi"],
            "http": ["HTTPClient", "WiFi", "ArduinoJson"],
            "ble": ["BLE", "NimBLE-Arduino"],
        }

        sensor_deps = {
            "temp_humidity": ["DHT", "SHT41"],
            "air_quality": ["BME680", "SGP30"],
            "motion": ["PIR", "MPU6050"],
            "light": ["BH1750", "TSL2561"],
        }

        deps = base_deps + protocol_deps.get(self.protocol, [])
        deps.extend(sensor_deps.get(self.sensor_type, []))

        return {
            "framework": "Arduino",
            "platform": "esp32",
            "dependencies": list(set(deps)),
            "config_files": [
                "config/platformio.ini",
                "config/mqtt_config.json",
                "config/sensor_config.json",
            ],
            "sensor_type": self.sensor_type,
            "communication_protocol": self.protocol,
            "features": [
                "OTA updates",
                "WiFi connectivity",
                f"{self.protocol.upper()} communication",
                "Sensor calibration",
                "Data logging",
                "Web dashboard support",
            ],
        }


class SHT41TemperatureHumidityTemplate(ESP32SensorTemplate):
    """Specialized template for SHT41 temperature and humidity sensor."""

    def __init__(self):
        """Initialize SHT41 sensor template."""
        super().__init__(sensor_type="temp_humidity", protocol="mqtt")

    def get_name(self) -> str:
        """Return the template's display name."""
        return "ESP32 SHT41 Environment Monitor"

    def get_description(self) -> str:
        """Return a short description of the template."""
        return (
            "Professional environment monitoring with SHT41 sensor. "
            "Includes temperature, humidity, and dew point calculation. "
            "MQTT integration ready."
        )

    def get_structure(self) -> Dict[str, Any]:
        """Return the project folder structure."""
        structure = super().get_structure()
        structure["docs"]["hardware"]["SHT41_datasheet.md"] = None
        structure["docs"]["software"]["dew_point_calculation.md"] = None
        structure["config"]["sht41_calibration.json"] = None
        return structure

    def get_metadata(self) -> Dict[str, Any]:
        """Return SHT41-specific metadata."""
        metadata = super().get_metadata()
        metadata["sensor_specs"] = {
            "model": "Sensirion SHT41",
            "interface": "I2C",
            "measurement_range": "-40 to +125 C",
            "humidity_range": "0 to 100 RH",
            "accuracy_temp": "+/-1.5 C",
            "accuracy_humidity": "+/-3 RH",
        }
        metadata["config_files"].append("config/sht41_calibration.json")
        return metadata


class BME680AirQualityTemplate(ESP32SensorTemplate):
    """Specialized template for BME680 air quality monitoring."""

    def __init__(self):
        """Initialize BME680 sensor template."""
        super().__init__(sensor_type="air_quality", protocol="mqtt")

    def get_name(self) -> str:
        """Return the template's display name."""
        return "ESP32 BME680 Air Quality Monitor"

    def get_description(self) -> str:
        """Return a short description of the template."""
        return (
            "Comprehensive air quality monitoring with BME680. "
            "Measures temperature, humidity, pressure, and VOC. "
            "Includes IAQ (Indoor Air Quality) calculation."
        )

    def get_structure(self) -> Dict[str, Any]:
        """Return the project folder structure."""
        structure = super().get_structure()
        structure["docs"]["hardware"]["BME680_datasheet.md"] = None
        structure["docs"]["software"]["iaq_calculation.md"] = None
        structure["examples"] = {
            "basic_reading.cpp": None,
            "with_calibration.cpp": None,
            "mqtt_publish.cpp": None,
        }
        return structure

    def get_metadata(self) -> Dict[str, Any]:
        """Return BME680-specific metadata."""
        metadata = super().get_metadata()
        metadata["sensor_specs"] = {
            "model": "Bosch BME680",
            "interface": "I2C/SPI",
            "temperature_range": "-40 to +85 C",
            "pressure_range": "300 to 1100 hPa",
            "humidity_range": "0 to 100 RH",
            "gas_range": "1 to 500k Ohm",
            "measurements": ["Temperature", "Humidity", "Pressure", "VOC"],
        }
        metadata["features"].extend([
            "IAQ index calculation",
            "VOC measurement",
            "Pressure trending",
        ])
        return metadata


class MotionSensorTemplate(ESP32SensorTemplate):
    """Template for ESP32 motion detection projects."""

    def __init__(self):
        """Initialize motion sensor template."""
        super().__init__(sensor_type="motion", protocol="mqtt")

    def get_name(self) -> str:
        """Return the template's display name."""
        return "ESP32 Motion Detection"

    def get_description(self) -> str:
        """Return a short description of the template."""
        return (
            "Motion detection and occupancy monitoring. "
            "PIR and accelerometer integration for reliable detection."
        )

    def get_metadata(self) -> Dict[str, Any]:
        """Return motion sensor metadata."""
        metadata = super().get_metadata()
        metadata["sensor_specs"] = {
            "primary": "PIR HC-SR501",
            "secondary": "MPU6050 Accelerometer",
            "interfaces": ["GPIO", "I2C"],
            "detection_range": "~7 meters",
        }
        metadata["features"].extend([
            "Dual sensor validation",
            "Occupancy tracking",
            "Motion statistics",
        ])
        return metadata


class LightSensorTemplate(ESP32SensorTemplate):
    """Template for ESP32 light level monitoring."""

    def __init__(self):
        """Initialize light sensor template."""
        super().__init__(sensor_type="light", protocol="mqtt")

    def get_name(self) -> str:
        """Return the template's display name."""
        return "ESP32 Light Level Monitor"

    def get_description(self) -> str:
        """Return a short description of the template."""
        return (
            "Ambient light monitoring and automatic control. "
            "BH1750 digital ambient light sensor integration."
        )

    def get_metadata(self) -> Dict[str, Any]:
        """Return light sensor metadata."""
        metadata = super().get_metadata()
        metadata["sensor_specs"] = {
            "model": "ROHM BH1750FVI",
            "interface": "I2C",
            "measurement_range": "1 to 65535 lux",
            "resolution": "1 lux",
            "response_time": "~16 ms",
        }
        metadata["features"].extend([
            "Automatic brightness control",
            "Lux-based triggers",
            "Low-power mode",
        ])
        return metadata


ESP32_TEMPLATES = {
    "generic": ESP32SensorTemplate,
    "sht41": SHT41TemperatureHumidityTemplate,
    "bme680": BME680AirQualityTemplate,
    "motion": MotionSensorTemplate,
    "light": LightSensorTemplate,
}
