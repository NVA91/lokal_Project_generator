"""ESP32 Sensor and IoT project templates."""

from __future__ import annotations
from typing import Any, Dict
from src.template_base import TemplateBase


class ESP32SensorTemplate(TemplateBase):
    """Base template for ESP32 sensor projects with MQTT integration."""

    def __init__(self, sensor_type: str = "generic", protocol: str = "mqtt", board: str = "esp32"):
        self.sensor_type = sensor_type
        self.protocol = protocol
        self.board = board

    def get_name(self) -> str:
        board_str = f" ({self.board.upper()})" if self.board != "esp32" else ""
        return f"ESP32 {self.sensor_type.title()} Sensor{board_str}"

    def get_description(self) -> str:
        protocol_upper = self.protocol.upper()
        return (
            f"ESP32 IoT project with {protocol_upper} on {self.board.upper()}. "
            f"Includes sensor calibration and data logging."
        )

    def get_structure(self) -> Dict[str, Any]:
        return {
            "src": {
                "main.cpp": None,
                "sensors": {f"{self.sensor_type}.cpp": None, f"{self.sensor_type}.h": None},
                "communication": {f"{self.protocol}.cpp": None, f"{self.protocol}.h": None},
            },
            "docs": {"hardware": {"pinout.md": None}, "README.md": None},
            "config": {"platformio.ini": None, "mqtt_config.json": None},
            "README.md": None,
        }

    def get_metadata(self) -> Dict[str, Any]:
        deps = ["esp32", "Arduino", "PlatformIO", "PubSubClient", "WiFi"]
        features = ["OTA updates", "WiFi", f"{self.protocol.upper()} integration"]

        if self.board == "esp32c6":
            features.extend(["Zigbee support", "Matter support"])
            deps.append("ESP32-C6-Arduino")
        elif self.board == "esp32s3":
            features.append("AI Vector instructions")
            deps.append("ESP32-S3-Arduino")

        return {
            "framework": "Arduino",
            "platform": self.board,
            "dependencies": list(set(deps)),
            "features": features,
            "sensor_type": self.sensor_type,
        }


class SHT41TemperatureHumidityTemplate(ESP32SensorTemplate):
    def __init__(self, board: str = "esp32"):
        super().__init__(sensor_type="temp_humidity", protocol="mqtt", board=board)

    def get_name(self) -> str:
        return f"ESP32 SHT41 Monitor ({self.board.upper()})"

    def get_metadata(self) -> Dict[str, Any]:
        metadata = super().get_metadata()
        metadata["sensor_specs"] = {"model": "SHT41", "accuracy": "+/-1.5 C"}
        return metadata


ESP32_TEMPLATES = {
    "generic": ESP32SensorTemplate,
    "sht41": SHT41TemperatureHumidityTemplate,
}
