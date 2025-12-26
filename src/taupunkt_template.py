"""Taupunkt Raspberry Pi Pico 2 dew point display template.

Specialized template for the taupunkt project - a MicroPython-based
dew point display system with multiple environmental sensors.
"""

from __future__ import annotations

from typing import Any, Dict
from .template_base import TemplateBase


class TaupunktTemplate(TemplateBase):
    """Template for Taupunkt Raspberry Pi Pico 2 dew point display.

    A MicroPython project featuring:
    - Dew point calculation and display
    - Multiple environmental sensors (AHT20, BMP280, SHT41)
    - ST7789 LCD display (1.47" 172x320)
    - Real-time sensor data visualization
    """

    def __init__(self):
        """Initialize Taupunkt template."""
        self.controller = "Raspberry Pi Pico 2"
        self.display = "Waveshare 1.47\" LCD ST7789"
        self.framework = "MicroPython"

    def get_name(self) -> str:
        """Return the template's display name."""
        return "Taupunkt - Dew Point Display"

    def get_description(self) -> str:
        """Return a short description of the template."""
        return (
            "MicroPython-based environmental monitoring and dew point "
            "display for Raspberry Pi Pico 2. Features AHT20, BMP280, "
            "and SHT41 sensors with ST7789 LCD output."
        )

    def get_structure(self) -> Dict[str, Any]:
        """Return the project folder structure."""
        return {
            "src": {
                "main.py": None,
                "config.py": None,
                "sensors": {
                    "aht20.py": None,
                    "bmp280.py": None,
                    "sht41.py": None,
                    "base_sensor.py": None,
                },
                "display": {
                    "lcd_st7789.py": None,
                    "ui.py": None,
                    "graphics.py": None,
                },
                "utils": {
                    "dew_point.py": None,
                    "calibration.py": None,
                    "logger.py": None,
                },
            },
            "micropython": {
                "lib": {
                    "st7789py.py": None,
                    "aht20.py": None,
                    "bmp280.py": None,
                },
                "main.py": None,
                "boot.py": None,
            },
            "docs": {
                "hardware": {
                    "pinout.md": None,
                    "wiring_diagram.md": None,
                    "bom.md": None,
                    "sensor_specs.md": None,
                    "display_specs.md": None,
                },
                "software": {
                    "dew_point_algorithm.md": None,
                    "sensor_calibration.md": None,
                    "micropython_setup.md": None,
                },
                "README.md": None,
            },
            "config": {
                "default_config.json": None,
                "sensor_offsets.json": None,
                "display_config.json": None,
            },
            "tests": {
                "test_sensors.py": None,
                "test_dew_point.py": None,
                "test_display.py": None,
            },
            "examples": {
                "basic_display.py": None,
                "with_logging.py": None,
                "advanced_ui.py": None,
            },
            "README.md": None,
            ".gitignore": None,
        }

    def get_metadata(self) -> Dict[str, Any]:
        """Return template metadata including dependencies."""
        return {
            "framework": "MicroPython",
            "platform": "Raspberry Pi Pico 2",
            "language": "Python 3",
            "dependencies": [
                "MicroPython",
                "micropython-st7789",
                "micropython-aht20",
                "micropython-bmp280",
                "micropython-sht41",
            ],
            "config_files": [
                "config/default_config.json",
                "config/sensor_offsets.json",
                "config/display_config.json",
            ],
            "sensors": {
                "primary_humidity_temp": "SHT41 (Indoor)",
                "secondary_humidity_temp": "AHT20 (Ambient)",
                "pressure": "BMP280",
            },
            "display": {
                "manufacturer": "Waveshare",
                "model": "1.47\" LCD",
                "controller": "ST7789",
                "resolution": "172x320",
                "interface": "SPI",
            },
            "controller_specs": {
                "model": "Raspberry Pi Pico 2",
                "processor": "ARM Cortex-M33",
                "frequency": "150 MHz",
                "ram": "520 KB",
                "flash": "4 MB",
                "gpio_pins": 26,
                "interfaces": ["SPI", "I2C", "UART"],
            },
            "features": [
                "Real-time dew point calculation",
                "Multi-sensor environmental monitoring",
                "Calibration support",
                "Data logging",
                "Low-power operation",
                "MicroPython optimized",
                "Graphical LCD display",
                "Sensor fusion",
            ],
            "pin_configuration": {
                "display_spi": "SPI0",
                "display_cs": "GPIO17",
                "display_dc": "GPIO18",
                "display_reset": "GPIO19",
                "sensor_i2c": "I2C1",
                "sensor_sda": "GPIO2",
                "sensor_scl": "GPIO3",
            },
            "dew_point_sensors": [
                {
                    "name": "SHT41",
                    "address": "0x44",
                    "type": "Indoor humidity/temperature",
                    "accuracy_temp": "+/-1.5 C",
                    "accuracy_humidity": "+/-3 RH",
                },
                {
                    "name": "AHT20",
                    "address": "0x38",
                    "type": "Ambient humidity/temperature",
                    "accuracy_temp": "+/-2 C",
                    "accuracy_humidity": "+/-5 RH",
                },
                {
                    "name": "BMP280",
                    "address": "0x76",
                    "type": "Barometric pressure",
                    "measurement_range": "300-1100 hPa",
                    "accuracy_pressure": "+/-1 hPa",
                },
            ],
            "calculation_algorithms": [
                "Magnus dew point approximation",
                "Sensor fusion for accuracy",
                "Temperature compensation",
                "Pressure-adjusted calculations",
            ],
        }


class TaupunktAdvancedTemplate(TaupunktTemplate):
    """Extended Taupunkt template with additional features.

    Includes web interface, cloud logging, and advanced analytics.
    """

    def get_name(self) -> str:
        """Return the template's display name."""
        return "Taupunkt Advanced - Cloud Connected"

    def get_description(self) -> str:
        """Return a short description of the template."""
        return (
            "Advanced MicroPython project with cloud connectivity, "
            "web interface, and data analytics. Includes MQTT, "
            "RESTful API, and long-term data logging."
        )

    def get_structure(self) -> Dict[str, Any]:
        """Return the advanced project structure."""
        structure = super().get_structure()
        # Add advanced features
        structure["src"]["connectivity"] = {
            "mqtt.py": None,
            "wifi.py": None,
            "api.py": None,
        }
        structure["src"]["storage"] = {
            "database.py": None,
            "cloud_sync.py": None,
        }
        structure["web"] = {
            "app.py": None,
            "templates": {
                "index.html": None,
                "dashboard.html": None,
            },
            "static": {
                "style.css": None,
                "chart.js": None,
            },
        }
        structure["docs"]["software"]["mqtt_integration.md"] = None
        structure["docs"]["software"]["web_api.md"] = None
        return structure

    def get_metadata(self) -> Dict[str, Any]:
        """Return advanced metadata."""
        metadata = super().get_metadata()
        metadata["dependencies"].extend([
            "micropython-mqtt",
            "micropython-requests",
            "micropython-json",
        ])
        metadata["features"].extend([
            "MQTT connectivity",
            "Web dashboard",
            "Cloud data sync",
            "RESTful API",
            "Historical analytics",
            "Real-time notifications",
        ])
        metadata["advanced_features"] = {
            "connectivity": ["WiFi", "MQTT", "REST API"],
            "storage": ["Local database", "Cloud sync"],
            "web_interface": ["Real-time dashboard", "Analytics"],
        }
        return metadata
