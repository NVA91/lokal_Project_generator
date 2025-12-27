"""Tests for ESP32 sensor templates."""

from src.esp32_templates import (
    ESP32SensorTemplate,
    SHT41TemperatureHumidityTemplate,
    ESP32_TEMPLATES,
)


class TestESP32SensorTemplate:
    def test_get_name(self):
        template = ESP32SensorTemplate(board="esp32c6")
        assert "ESP32C6" in template.get_name()

    def test_metadata_c6(self):
        template = ESP32SensorTemplate(board="esp32c6")
        meta = template.get_metadata()
        assert "Zigbee support" in meta["features"]


class TestSHT41Template:
    def test_sensor_specs(self):
        template = SHT41TemperatureHumidityTemplate()
        meta = template.get_metadata()
        assert meta["sensor_specs"]["model"] == "SHT41"


class TestESP32TemplateRegistry:
    def test_registry_content(self):
        # Benutzt ESP32_TEMPLATES, damit flake8 nicht meckert
        assert "sht41" in ESP32_TEMPLATES
        assert ESP32_TEMPLATES["sht41"] == SHT41TemperatureHumidityTemplate
