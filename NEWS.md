# News & Changelog

## Latest: Taupunkt Template Integration 🎉

### Added

#### Template Registry System
- New `TemplateRegistry` class for dynamic template management
- Programmatic template discovery and instantiation
- Template metadata inspection (structure, dependencies, features)
- Convenience functions for common operations

#### Taupunkt Template
- **Taupunkt** - Raspberry Pi Pico 2 dew point display system
  - Real-time environmental monitoring
  - Multi-sensor support (AHT20, BMP280, SHT41)
  - ST7789 LCD display output
  - MicroPython optimized
  - Local data logging

- **Taupunkt Advanced** - Extended variant with cloud features
  - MQTT connectivity
  - Web dashboard
  - RESTful API
  - Cloud data synchronization
  - Real-time analytics

#### Documentation
- `TEMPLATE_REGISTRY.md` - Registry system documentation and API reference
- `docs/TAUPUNKT_TEMPLATE.md` - Comprehensive Taupunkt template guide
  - Hardware specifications and pinout
  - Project structure explanation
  - Configuration file documentation
  - Usage examples and code snippets
  - Dew point calculation algorithm
  - Troubleshooting guide

#### Examples
- `examples/taupunkt_example.py` - Practical usage examples
  - Template discovery
  - Structure inspection
  - Metadata examination
  - Project generation workflow

#### Code Files
- `src/taupunkt_template.py` - Template implementation (9000+ lines)
- `src/template_registry.py` - Registry system (160+ lines)
- Updated `src/__init__.py` - Package exports

### Details

#### Taupunkt Hardware Configuration

| Component | Specification |
|-----------|---------------|
| Controller | Raspberry Pi Pico 2 (ARM Cortex-M33 @ 150MHz) |
| Display | Waveshare 1.47" LCD ST7789 (172×320) |
| Temperature (Primary) | SHT41 (±1.5°C) |
| Temperature (Secondary) | AHT20 (±2°C) |
| Humidity (Primary) | SHT41 (±3% RH) |
| Humidity (Secondary) | AHT20 (±5% RH) |
| Pressure | BMP280 (±1 hPa, 300-1100 hPa) |
| Interface | I2C (sensors), SPI (display) |

#### Taupunkt Features

- ✅ Real-time dew point calculation (Magnus algorithm)
- ✅ Sensor fusion for improved accuracy
- ✅ Per-sensor calibration and offset support
- ✅ Graphical LCD display with custom UI
- ✅ Local data logging
- ✅ MicroPython optimized (minimal RAM usage)
- ✅ Modular sensor drivers
- ✅ Comprehensive documentation

#### Taupunkt Advanced Features

- ✅ All basic features
- ✅ WiFi connectivity
- ✅ MQTT publishing
- ✅ RESTful API server
- ✅ Web dashboard (HTML/JS)
- ✅ Cloud data synchronization
- ✅ Historical data analytics
- ✅ Real-time notifications

### Structure Highlights

#### Template Organization

```
✅ Sensor drivers (AHT20, BMP280, SHT41)
✅ Display drivers (ST7789 with UI layer)
✅ Utility modules (dew point calc, calibration, logging)
✅ MicroPython deployment files
✅ Comprehensive documentation
✅ Configuration templates
✅ Unit test stubs
✅ Usage examples
```

### Breaking Changes

None. This is a new feature addition that maintains backward compatibility.

### Migration Guide

No migration needed. Existing templates continue to work as before.

New templates are registered programmatically in `TemplateRegistry`.

### Future Roadmap

- [ ] Template versioning
- [ ] Dependency resolution
- [ ] Template marketplace integration
- [ ] GUI template selector
- [ ] Configuration wizard for templates
- [ ] Template validation and testing framework
- [ ] Cloud template repository

### Getting Started with Taupunkt

1. **Explore Templates**:
   ```python
   from src.template_registry import list_templates
   print(list_templates())
   ```

2. **Inspect Taupunkt**:
   ```python
   from src.template_registry import get_template_info
   info = get_template_info("taupunkt")
   print(info['metadata'])
   ```

3. **Create Project**:
   ```python
   template = get_template("taupunkt")
   structure = template.get_structure()
   # Generate files based on structure
   ```

4. **See Examples**:
   ```bash
   python examples/taupunkt_example.py
   ```

5. **Read Docs**:
   - Registry: `TEMPLATE_REGISTRY.md`
   - Taupunkt: `docs/TAUPUNKT_TEMPLATE.md`

### Credits

- Taupunkt project: [github.com/NVA91/taupunkt](https://github.com/NVA91/taupunkt)
- Template system: lokal_Project_generator improvements

### Support

- Issues and questions: GitHub Issues
- Documentation: See `docs/` and root `*.md` files
- Examples: See `examples/` directory

---

*Release Date: 2025-12-26*
*Integration: lokal_Project_generator v2.0+*
