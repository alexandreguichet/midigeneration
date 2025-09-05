# 🎼 MIDI Generation System

A flexible, configuration-driven MIDI composition generator for creating jazz piano arrangements with sophisticated melodic variations.

## 🚀 Quick Start

```bash
# Generate a jazz composition
python midi.py jazz_config.json

# Analyze the generated MIDI
python utils/midi_analyzer.py jazz_variations.mid
```

## 📁 Project Structure

```
├── 📜 midi.py                    # Main MIDI generator
│
├── 📁 config/                    # Configuration files
│   ├── jazz_config.json
│   └── simple_ballad_config.json
│
├── 📁 utils/                     # Analysis and utility tools
│   ├── midi_analyzer.py         # MIDI file analyzer
│   └── midi_inspector.py        # Detailed MIDI inspector
│
├── 📁 output/                    # Generated MIDI files
│   └── *.mid                    # (auto-generated)
│
└── 📁 docs/                      # Documentation
    ├── README.md                 # Detailed documentation
    └── JAZZ_VARIATIONS_GUIDE.md  # Jazz variations guide
```

## 🎵 Features

- **🎹 Jazz Piano Arrangements**: Professional chord voicings and progressions
- **🎶 Melodic Variations**: Multiple right-hand styles (comping, melody, solo)
- **🎯 Configurable**: JSON-based configuration system
- **📊 Analysis Tools**: Comprehensive MIDI file analysis
- **📁 Organized Structure**: Clean separation of configs, outputs, docs, and utilities

## 🎼 Available Configurations

- **`jazz_config.json`**: 28-bar jazz piece with intro/verse/solo/bridge
- **`simple_ballad_config.json`**: Gentle ballad arrangement

## 🔧 Usage Examples

### Generate from Config
```bash
# Use config filename (automatically checks config/ folder)
python midi.py jazz_config.json

# Or use full path
python midi.py config/jazz_config.json
```

### Analyze Generated MIDI
```bash
# Analyzer automatically checks output/ folder
python utils/midi_analyzer.py jazz_variations.mid

# Detailed inspection
python utils/midi_inspector.py jazz_variations.mid
```

### List Available Configs
```bash
# Run without arguments to see available configs and tools
python midi.py
```

## 📖 Documentation

- **[📚 Full Documentation](docs/README.md)**: Complete API and configuration guide
- **[🎵 Jazz Variations Guide](docs/JAZZ_VARIATIONS_GUIDE.md)**: Jazz-specific features and examples

## 🎯 Requirements

```bash
pip install mido
```

## 🎨 Quick Example

```python
from midi import ConfigurableMIDIGenerator

# Create generator
generator = ConfigurableMIDIGenerator()

# Load and generate
generator.load_configuration('config/jazz_config.json')
output_file = generator.create_composition()

print(f"Generated: {output_file}")
```

## 🏗️ Project Organization

### **Core Files**
- `midi.py` - Main MIDI generation engine

### **Configuration** (`config/`)
- JSON files defining musical content and arrangements

### **Utilities** (`utils/`)
- Analysis and debugging tools for generated MIDI files

### **Output** (`output/`)
- Auto-generated MIDI files (ignored by git)

### **Documentation** (`docs/`)
- Comprehensive guides and API documentation

---
*Generate professional-quality MIDI compositions with ease! 🎹✨*
