# Taupunkt Template Documentation

The Taupunkt template is a specialized project generator for Raspberry Pi Pico 2-based dew point monitoring systems.

## Overview

Taupunkt is a comprehensive MicroPython solution for environmental monitoring with emphasis on dew point calculation. It combines multiple sensors to provide accurate atmospheric measurements.

### Key Features

- **Real-time Dew Point Calculation** - Magnus approximation algorithm with sensor fusion
- **Multi-Sensor Support** - AHT20, BMP280, and SHT41 environmental sensors
- **Graphical Display** - ST7789 LCD output (1.47" 172x320)
- **Calibration Support** - Per-sensor offset and correction factors
- **Data Logging** - Local storage with optional cloud sync (Advanced variant)
- **MicroPython Optimized** - Efficient code for embedded systems

## Hardware Configuration

### Main Controller

| Specification | Value |
|---------------|-------|
| Model | Raspberry Pi Pico 2 |
| Processor | ARM Cortex-M33 |
| Frequency | 150 MHz |
| RAM | 520 KB |
| Flash Storage | 4 MB |
| GPIO Pins | 26 |
| Interfaces | SPI, I2C, UART |

### Display

| Specification | Value |
|---------------|-------|
| Manufacturer | Waveshare |
| Size | 1.47" |
| Controller | ST7789 |
| Resolution | 172 × 320 pixels |
| Interface | SPI |
| Colors | 16-bit RGB565 |

### Sensors

#### SHT41 (Indoor Humidity/Temperature)
- **Address**: 0x44
- **Temperature Range**: -45°C to +130°C
- **Humidity Range**: 0-100% RH
- **Temperature Accuracy**: ±1.5°C
- **Humidity Accuracy**: ±3% RH
- **Interface**: I2C

#### AHT20 (Ambient Humidity/Temperature)
- **Address**: 0x38
- **Temperature Range**: -40°C to +80°C
- **Humidity Range**: 0-100% RH
- **Temperature Accuracy**: ±2°C
- **Humidity Accuracy**: ±5% RH
- **Interface**: I2C

#### BMP280 (Barometric Pressure)
- **Address**: 0x76
- **Pressure Range**: 300-1100 hPa
- **Temperature Range**: -40°C to +85°C
- **Pressure Accuracy**: ±1 hPa
- **Interface**: I2C

## Pin Configuration

### SPI (Display)

```
Display (ST7789)
├── CS   → GPIO 17
├── DC   → GPIO 18
├── Reset → GPIO 19
└── SPI0 → Standard pins
```

### I2C (Sensors)

```
Sensors (I2C1)
├── SDA → GPIO 2
├── SCL → GPIO 3
├── SHT41 → 0x44
├── AHT20 → 0x38
└── BMP280 → 0x76
```

## Project Structure

### Basic Template

```
taupunkt/
├── src/
│   ├── main.py              # Entry point
│   ├── config.py            # Configuration
│   ├── sensors/             # Sensor drivers
│   │   ├── aht20.py
│   │   ├── bmp280.py
│   │   ├── sht41.py
│   │   └── base_sensor.py
│   ├── display/             # Display drivers
│   │   ├── lcd_st7789.py
│   │   ├── ui.py
│   │   └── graphics.py
│   └── utils/               # Utilities
│       ├── dew_point.py     # Calculation algorithms
│       ├── calibration.py
│       └── logger.py
├── micropython/             # Device code
│   ├── lib/                 # Device libraries
│   ├── main.py              # Device main script
│   └── boot.py              # Device boot script
├── docs/
│   ├── hardware/            # Hardware documentation
│   └── software/            # Software guides
├── config/                  # Configuration files
│   ├── default_config.json
│   ├── sensor_offsets.json
│   └── display_config.json
├── tests/                   # Unit tests
├── examples/                # Usage examples
└── README.md
```

## Dependencies

### Core MicroPython Libraries

```python
machine              # GPIO, SPI, I2C control
time                # Timing functions
json                # Configuration parsing
struct              # Binary data parsing
```

### Third-party Libraries

- `micropython-st7789` - Display driver
- `micropython-aht20` - AHT20 sensor driver
- `micropython-bmp280` - BMP280 sensor driver
- `micropython-sht41` - SHT41 sensor driver

### Advanced Template (Optional)

- `micropython-mqtt` - MQTT connectivity
- `micropython-requests` - HTTP/REST API
- `micropython-json` - JSON utilities

## Dew Point Calculation

### Magnus Approximation Formula

The dew point is calculated using the Magnus approximation:

```
γ(T,RH) = ln(RH/100) + (a*T)/(b+T)
Td = (b*γ(T,RH))/(a-γ(T,RH))
```

Where:
- `T` = Temperature in °C
- `RH` = Relative humidity in %
- `a` = 17.27
- `b` = 237.7
- `Td` = Dew point temperature in °C

### Sensor Fusion

The template supports combining readings from multiple sensors:

1. **Primary** (SHT41): Most accurate, used for dew point calculation
2. **Secondary** (AHT20): Cross-validation and redundancy
3. **Pressure** (BMP280): Pressure-adjusted calculations

## Usage Examples

### Basic Setup

```python
from src.sensors import SHT41, AHT20, BMP280
from src.utils import DewPointCalculator
from src.display import LCD

# Initialize sensors
sht41 = SHT41(i2c=i2c_bus)
aht20 = AHT20(i2c=i2c_bus)
bmp280 = BMP280(i2c=i2c_bus)

# Initialize display
display = LCD(spi=spi_bus)

# Read data
temp = sht41.read_temperature()
humidity = sht41.read_humidity()
pressure = bmp280.read_pressure()

# Calculate dew point
dewd = DewPointCalculator.calculate(temp, humidity)

# Display result
display.show_dew_point(temp, humidity, dew_point)
```

### With Calibration

```python
from src.utils import Calibration

# Load calibration offsets
calibration = Calibration.from_file('config/sensor_offsets.json')

# Apply corrections
temp_corrected = temp + calibration.sht41['temp_offset']
humidity_corrected = humidity + calibration.sht41['humidity_offset']

# Calculate with corrected values
dew_point = DewPointCalculator.calculate(temp_corrected, humidity_corrected)
```

### Advanced: Cloud Integration (Advanced Template)

```python
from src.connectivity import MQTT
from src.utils import DataLogger

# Initialize MQTT
mqtt = MQTT(broker='home.local', client_id='taupunkt_01')
mqtt.connect()

# Initialize data logger
logger = DataLogger('config/default_config.json')

# Publish readings
mqtt.publish('home/taupunkt/temperature', temp)
mqtt.publish('home/taupunkt/humidity', humidity)
mqtt.publish('home/taupunkt/dew_point', dew_point)

# Log locally
logger.log({'temp': temp, 'humidity': humidity, 'dew_point': dew_point})
```

## Configuration Files

### default_config.json

```json
{
  "display": {
    "update_interval_ms": 2000,
    "brightness": 255,
    "rotation": 0
  },
  "sensors": {
    "poll_interval_ms": 2000,
    "sht41_enabled": true,
    "aht20_enabled": true,
    "bmp280_enabled": true
  },
  "dew_point": {
    "algorithm": "magnus",
    "use_sensor_fusion": true
  }
}
```

### sensor_offsets.json

```json
{
  "sht41": {
    "temp_offset": 0.0,
    "humidity_offset": 0.0
  },
  "aht20": {
    "temp_offset": 0.0,
    "humidity_offset": 0.0
  },
  "bmp280": {
    "pressure_offset": 0.0
  }
}
```

## Getting Started

### 1. Hardware Assembly

- Connect display via SPI0 (CS, DC, Reset)
- Connect sensors via I2C1 (SDA, SCL)
- Ensure proper power distribution and decoupling capacitors

### 2. MicroPython Installation

```bash
# Download MicroPython for Pico 2
wget https://micropython.org/download/rp2/firmware.uf2

# Copy to Pico (hold BOOTSEL during connect)
# Mount Pico, copy firmware.uf2
```

### 3. Upload Project

```bash
# Copy micropython folder contents to device
ampy -p /dev/ttyUSB0 put micropython/boot.py
ampy -p /dev/ttyUSB0 put micropython/main.py

# Copy libraries
ampy -p /dev/ttyUSB0 put micropython/lib/ -r
```

### 4. Verify Operation

```python
# From REPL
import main
main.run()
```

## Template Variants

### Taupunkt (Basic)
Core dew point display functionality with local storage.

**Use when:**
- Standalone monitoring
- Local display only
- Minimal dependencies

### Taupunkt Advanced
Extended features with cloud connectivity and analytics.

**Use when:**
- Remote monitoring needed
- Data archival required
- Web dashboard desired
- MQTT integration needed

## Troubleshooting

### Sensor not detected

1. Check I2C connections (SDA, SCL)
2. Verify pull-up resistors (typically 4.7k)
3. Scan I2C bus: `i2c.scan()`
4. Confirm address (SHT41=0x44, AHT20=0x38, BMP280=0x76)

### Display not showing

1. Check SPI connections (MOSI, MISO, CLK, CS, DC, Reset)
2. Verify GPIO pin assignments
3. Test display with initialization code
4. Check ST7789 controller communication

### Inaccurate readings

1. Run calibration routine
2. Update sensor offset configuration
3. Verify sensor placement (not near heat sources)
4. Check sensor age and validity

## References

- [Raspberry Pi Pico 2 Documentation](https://www.raspberrypi.com/documentation/microcontrollers/pico.html)
- [MicroPython Documentation](https://docs.micropython.org/)
- [Magnus Formula](https://en.wikipedia.org/wiki/Dew_point#Magnus_formula)
- [Waveshare LCD Documentation](https://www.waveshare.com/1.47inch-lcd-module.htm)

## License

See LICENSE file in project root.
