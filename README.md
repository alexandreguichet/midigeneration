# 🎼 MIDI Generation System

A flexible, configuration-driven MIDI composition generator for creating jazz piano arrangements with sophisticated melodic variations.

## 🚀 Quick Start with Poetry

### Prerequisites
- Python 3.9+ 
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management

### Installation
```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Clone the repository
git clone https://github.com/alexandreguichet/midigeneration.git
cd midigeneration

# Install dependencies
poetry install
```

### Usage
```bash
# Generate a jazz composition
poetry run midi-generate jazz_config.json

# Or use the main script directly
poetry run python main.py jazz_config.json

# Analyze the generated MIDI
poetry run python utils/midi_analyzer.py jazz_variations.mid
```

## 📁 Project Structure

```
├── 📜 main.py                    # Main launcher script
├── 📦 pyproject.toml             # Poetry configuration & dependencies
├── 🧪 run_tests.py               # Test runner with coverage
│
├── 📁 src/                       # Source code
│   ├── __init__.py
│   └── midi.py                   # Main MIDI generator
│
├── 📁 config/                    # Configuration files
│   ├── jazz_config.json
│   └── simple_ballad_config.json
│
├── 📁 utils/                     # Analysis and utility tools
│   ├── midi_analyzer.py         # MIDI file analyzer
│   └── midi_inspector.py        # Detailed MIDI inspector
│
├── 📁 test/                      # Unit tests
│   ├── __init__.py
│   └── test_midi.py              # Comprehensive test suite
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
- **🧪 100% Test Coverage**: Comprehensive unit tests with coverage reporting
- **📦 Poetry Management**: Modern Python dependency management
- **🔍 Code Quality**: Black, isort, flake8, mypy integration

## 🎼 Available Configurations

- **`jazz_config.json`**: 28-bar jazz piece with intro/verse/solo/bridge
- **`simple_ballad_config.json`**: Gentle ballad arrangement

## 🔧 Development Commands

### Testing & Quality Assurance
```bash
# Run all tests with coverage
poetry run python run_tests.py

# Run only tests
poetry run python run_tests.py --test-only

# Run only linting/code quality checks
poetry run python run_tests.py --lint-only

# Run tests directly with pytest
poetry run pytest

# Generate coverage report
poetry run pytest --cov=src --cov-report=html
```

### Code Formatting & Linting
```bash
# Format code with Black
poetry run black src/ test/

# Sort imports with isort
poetry run isort src/ test/

# Lint with flake8
poetry run flake8 src/ test/

# Type checking with mypy
poetry run mypy src/
```

### Usage Examples
```bash
# Generate from config (automatically checks config/ folder)
poetry run midi-generate jazz_config.json
poetry run python main.py jazz_config.json

# Or use full path
poetry run midi-generate config/jazz_config.json

# Analyze generated MIDI (automatically checks output/ folder)
poetry run python utils/midi_analyzer.py jazz_variations.mid

# Detailed inspection
poetry run python utils/midi_inspector.py jazz_variations.mid

# List available configs and tools
poetry run python main.py
```

## 📖 Documentation

- **[📚 Full Documentation](docs/README.md)**: Complete API and configuration guide
- **[🎵 Jazz Variations Guide](docs/JAZZ_VARIATIONS_GUIDE.md)**: Jazz-specific features and examples

## 🧪 Testing

The project includes comprehensive unit tests with 100% code coverage:

- **Unit Tests**: Complete test suite for all classes and functions
- **Coverage Reporting**: HTML and LCOV coverage reports
- **Continuous Integration**: Ready for CI/CD pipelines
- **Mock Testing**: Comprehensive mocking of external dependencies

## 🎨 API Usage

```python
from src.midi import ConfigurableMIDIGenerator

# Create generator
generator = ConfigurableMIDIGenerator()

# Load and generate
generator.load_configuration('config/jazz_config.json')
output_file = generator.create_composition()

print(f"Generated: {output_file}")
```

## 🏗️ Project Organization

### **Source Code** (`src/`)
- `midi.py` - Main MIDI generation engine

### **Configuration** (`config/`)
- JSON files defining musical content and arrangements

### **Utilities** (`utils/`)
- Analysis and debugging tools for generated MIDI files

### **Tests** (`test/`)
- Comprehensive unit test suite with mocking

### **Output** (`output/`)
- Auto-generated MIDI files (ignored by git)

### **Documentation** (`docs/`)
- Comprehensive guides and API documentation

## 📦 Dependencies

### Runtime Dependencies
- **mido**: MIDI file manipulation library

### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **coverage**: Coverage measurement
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

## 🤝 Contributing

1. **Setup development environment**:
   ```bash
   poetry install
   ```

2. **Run tests before committing**:
   ```bash
   poetry run python run_tests.py
   ```

3. **Format code**:
   ```bash
   poetry run black src/ test/
   poetry run isort src/ test/
   ```

4. **Check code quality**:
   ```bash
   poetry run flake8 src/ test/
   poetry run mypy src/
   ```

---
*Generate professional-quality MIDI compositions with ease! 🎹✨*
