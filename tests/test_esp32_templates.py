"""Tests for ESP32 sensor templates."""

import pytest
from src.esp32_templates import (
    ESP32SensorTemplate,
    SHT41TemperatureHumidityTemplate,
    BME680AirQualityTemplate,
    MotionSensorTemplate,
    LightSensorTemplate,
    ESP32_TEMPLATES,
)


class TestESP32SensorTemplate:
    """Test cases for base ESP32SensorTemplate."""

    def test_init_default_parameters(self):
        """Test initialization with default parameters."""
        template = ESP32SensorTemplate()
        assert template.sensor_type == "generic"
        assert template.protocol == "mqtt"

    def test_init_custom_parameters(self):
        """Test initialization with custom parameters."""
        template = ESP32SensorTemplate(
            sensor_type="temp_humidity", protocol="http"
        )
        assert template.sensor_type == "temp_humidity"
        assert template.protocol == "http"

    def test_get_name(self):
        """Test template name generation."""
        template = ESP32SensorTemplate(sensor_type="motion")
        assert "Motion" in template.get_name()
        assert "ESP32" in template.get_name()

    def test_get_description(self):
        """Test template description."""
        template = ESP32SensorTemplate(protocol="mqtt")
        desc = template.get_description()
        assert "MQTT" in desc
        assert "ESP32" in desc

    def test_get_structure(self):
        """Test project structure generation."""
        template = ESP32SensorTemplate()
        structure = template.get_structure()

        # Verify key directories exist
        assert "src" in structure
        assert "docs" in structure
        assert "config" in structure
        assert "tests" in structure

        # Verify nested structure
        assert "sensors" in structure["src"]
        assert "communication" in structure["src"]
        assert "utils" in structure["src"]

        # Verify documentation structure
        assert "hardware" in structure["docs"]
        assert "software" in structure["docs"]

    def test_get_metadata(self):
        """Test metadata generation."""
        template = ESP32SensorTemplate(
            sensor_type="temp_humidity", protocol="mqtt"
        )
        metadata = template.get_metadata()

        # Verify required fields
        assert "dependencies" in metadata
        assert "config_files" in metadata
        assert "framework" in metadata
        assert "platform" in metadata

        # Verify values
        assert "esp32" in metadata["platform"]
        assert "Arduino" in metadata["framework"]
        assert "SHT41" in metadata["dependencies"]
        assert "PubSubClient" in metadata["dependencies"]


class TestSHT41Template:
    """Test cases for SHT41 specialized template."""

    def test_init(self):
        """Test SHT41 template initialization."""
        template = SHT41TemperatureHumidityTemplate()
        assert template.sensor_type == "temp_humidity"
        assert template.protocol == "mqtt"

    def test_get_name(self):
        """Test SHT41 name includes sensor model."""
        template = SHT41TemperatureHumidityTemplate()
        assert "SHT41" in template.get_name()
        assert "Environment Monitor" in template.get_name()

    def test_get_description(self):
        """Test SHT41 description mentions specific features."""
        template = SHT41TemperatureHumidityTemplate()
        desc = template.get_description()
        assert "SHT41" in desc
        assert "dew point" in desc.lower()

    def test_get_structure_includes_sht41_docs(self):
        """Test structure includes SHT41-specific documentation."""
        template = SHT41TemperatureHumidityTemplate()
        structure = template.get_structure()
        assert "SHT41_datasheet.md" in structure["docs"]["hardware"]
        assert "dew_point_calculation.md" in structure["docs"]["software"]
        assert "sht41_calibration.json" in structure["config"]

    def test_get_metadata_includes_sensor_specs(self):
        """Test metadata includes detailed sensor specifications."""
        template = SHT41TemperatureHumidityTemplate()
        metadata = template.get_metadata()

        assert "sensor_specs" in metadata
        specs = metadata["sensor_specs"]
        assert specs["model"] == "Sensirion SHT41"
        assert specs["interface"] == "I2C"
        assert "accuracy" in specs["accuracy_temp"].lower()


class TestBME680Template:
    """Test cases for BME680 specialized template."""

    def test_init(self):
        """Test BME680 template initialization."""
        template = BME680AirQualityTemplate()
        assert template.sensor_type == "air_quality"

    def test_get_name(self):
        """Test BME680 name is descriptive."""
        template = BME680AirQualityTemplate()
        assert "BME680" in template.get_name()
        assert "Air Quality" in template.get_name()

    def test_get_structure_includes_examples(self):
        """Test structure includes example code."""
        template = BME680AirQualityTemplate()
        structure = template.get_structure()
        assert "examples" in structure
        assert "basic_reading.cpp" in structure["examples"]
        assert "mqtt_publish.cpp" in structure["examples"]

    def test_get_metadata_has_iaq_feature(self):
        """Test metadata includes IAQ feature."""
        template = BME680AirQualityTemplate()
        metadata = template.get_metadata()
        assert "IAQ index calculation" in metadata["features"]
        assert "VOC measurement" in metadata["features"]

    def test_sensor_specs_include_all_measurements(self):
        """Test BME680 specs list all measurement types."""
        template = BME680AirQualityTemplate()
        metadata = template.get_metadata()
        measurements = metadata["sensor_specs"]["measurements"]
        assert "Temperature" in measurements
        assert "Humidity" in measurements
        assert "Pressure" in measurements
        assert "VOC" in measurements


class TestMotionTemplate:
    """Test cases for motion sensor template."""

    def test_get_name(self):
        """Test motion template name."""
        template = MotionSensorTemplate()
        assert "Motion Detection" in template.get_name()

    def test_sensor_specs(self):
        """Test motion sensor specifications."""
        template = MotionSensorTemplate()
        metadata = template.get_metadata()
        specs = metadata["sensor_specs"]
        assert "PIR HC-SR501" in specs["primary"]
        assert "MPU6050" in specs["secondary"]

    def test_features_include_dual_validation(self):
        """Test dual sensor validation feature."""
        template = MotionSensorTemplate()
        metadata = template.get_metadata()
        assert "Dual sensor validation" in metadata["features"]
        assert "Occupancy tracking" in metadata["features"]


class TestLightTemplate:
    """Test cases for light sensor template."""

    def test_get_name(self):
        """Test light template name."""
        template = LightSensorTemplate()
        assert "Light Level Monitor" in template.get_name()

    def test_sensor_model(self):
        """Test light sensor model in specs."""
        template = LightSensorTemplate()
        metadata = template.get_metadata()
        assert metadata["sensor_specs"]["model"] == "ROHM BH1750FVI"

    def test_lux_measurement_range(self):
        """Test lux measurement range."""
        template = LightSensorTemplate()
        metadata = template.get_metadata()
        spec_range = metadata["sensor_specs"]["measurement_range"]
        assert "1" in spec_range and "65535 lux" in spec_range


class TestESP32TemplateRegistry:
    """Test cases for ESP32 template registry."""

    def test_registry_exists(self):
        """Test that template registry is defined."""
        assert ESP32_TEMPLATES is not None
        assert isinstance(ESP32_TEMPLATES, dict)

    def test_registry_has_all_templates(self):
        """Test registry contains all template classes."""
        assert "generic" in ESP32_TEMPLATES
        assert "sht41" in ESP32_TEMPLATES
        assert "bme680" in ESP32_TEMPLATES
        assert "motion" in ESP32_TEMPLATES
        assert "light" in ESP32_TEMPLATES

    def test_registry_instantiation(self):
        """Test that registry templates can be instantiated."""
        for template_key, template_class in ESP32_TEMPLATES.items():
            template = template_class()
            assert template is not None
            assert hasattr(template, "get_name")
            assert hasattr(template, "get_metadata")


class TestTemplateConsistency:
    """Test consistency across all ESP32 templates."""

    @pytest.fixture
    def all_templates(self):
        """Fixture providing all template instances."""
        return [
            ESP32SensorTemplate(),
            SHT41TemperatureHumidityTemplate(),
            BME680AirQualityTemplate(),
            MotionSensorTemplate(),
            LightSensorTemplate(),
        ]

    def test_all_templates_have_name(self, all_templates):
        """Test all templates provide a name."""
        for template in all_templates:
            name = template.get_name()
            assert isinstance(name, str)
            assert len(name) > 0

    def test_all_templates_have_description(self, all_templates):
        """Test all templates provide a description."""
        for template in all_templates:
            desc = template.get_description()
            assert isinstance(desc, str)
            assert len(desc) > 0

    def test_all_templates_have_structure(self, all_templates):
        """Test all templates provide project structure."""
        for template in all_templates:
            structure = template.get_structure()
            assert isinstance(structure, dict)
            assert len(structure) > 0

    def test_all_templates_have_metadata(self, all_templates):
        """Test all templates provide metadata."""
        for template in all_templates:
            metadata = template.get_metadata()
            assert isinstance(metadata, dict)
            assert "dependencies" in metadata
            assert "config_files" in metadata

    def test_all_structures_have_required_dirs(self, all_templates):
        """Test all structures include required directories."""
        required_dirs = ["src", "docs", "config", "README.md"]
        for template in all_templates:
            structure = template.get_structure()
            for required in required_dirs:
                assert required in structure, (
                    f"{template.get_name()} missing {required}"
                )

    def test_all_metadata_include_features(self, all_templates):
        """Test all metadata include feature list."""
        for template in all_templates:
            metadata = template.get_metadata()
            assert "features" in metadata
            assert isinstance(metadata["features"], list)
            assert len(metadata["features"]) > 0
