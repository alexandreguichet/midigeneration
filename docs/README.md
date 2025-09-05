# 📚 MIDI Generation System - Complete Documentation

## 🎼 Overview

This system provides a flexible, JSON-driven approach to generating professional MIDI compositions, with a focus on jazz piano arrangements.

## 🏗️ System Architecture

### Core Components

1. **`ConfigurableMIDIGenerator`** - Main composition engine
2. **JSON Configuration System** - Defines musical content
3. **Pattern Engine** - Handles rhythm and timing
4. **Analysis Tools** - MIDI file inspection and validation

### File Organization

```
midi-generation/
├── midi.py                           # 🎼 Main generator
│
├── config/                           # ⚙️  Configuration files
│   ├── jazz_config.json
│   └── simple_ballad_config.json
│
├── utils/                            # � Analysis and utility tools
│   ├── midi_analyzer.py             # 🔍 Analysis tool
│   └── midi_inspector.py            # 🔍 Detailed inspector
│
├── output/                           # 📁 Generated MIDI files
│   └── *.mid                        # (auto-generated)
│
└── docs/                             # 📚 Documentation
    ├── README.md                     # (this file)
    └── JAZZ_VARIATIONS_GUIDE.md      # Jazz-specific guide
```

## ⚙️ Configuration System

### JSON Structure

```json
{
  "metadata": {
    "title": "Composition Name",
    "tempo": 125,
    "time_signature": [4, 4],
    "ticks_per_beat": 480,
    "output_filename": "output_name.mid"
  },
  "chord_progressions": {
    "structure": ["intro", "verse", "solo", "bridge"],
    "sections": {
      "intro": ["Cm7", "Fm7", "G7", "Cm7"],
      "verse": ["Cm7", "F7", "BbMaj7", "EbMaj7"]
    }
  },
  "chord_voicings": {
    "Cm7": {
      "right_hand": [67, 70, 75],
      "right_hand_melody": [72, 75, 77, 75, 72, 70, 67, 70],
      "right_hand_solo": [72, 74, 75, 77, 79, 77, 75, 74],
      "left_hand": {
        "bass": 48,
        "chord": [55, 58, 63]
      }
    }
  },
  "patterns": {
    "intro": {
      "right_hand": [1, 0, 0, 1, 0, 1, 0, 0],
      "left_hand": [2, 0, 1, 1, 1, 0, 0, 0],
      "rh_velocity": 75,
      "lh_velocity": 65,
      "melody_type": "chord"
    }
  }
}
```

### Configuration Sections

#### 1. Metadata
- **title**: Composition name (appears in MIDI track)
- **tempo**: BPM (beats per minute)
- **time_signature**: [numerator, denominator]
- **ticks_per_beat**: MIDI timing resolution
- **output_filename**: Generated file name

#### 2. Chord Progressions
- **structure**: Array of section names in order
- **sections**: Object mapping section names to chord arrays

#### 3. Chord Voicings
Each chord contains:
- **right_hand**: Notes for chord comping
- **right_hand_melody**: 8-note melodic phrase
- **right_hand_solo**: 16-note solo runs
- **left_hand.bass**: Root note (MIDI number)
- **left_hand.chord**: 3-note chord voicing

#### 4. Patterns
Per-section rhythm patterns:
- **right_hand**: 16-position array (16th note grid)
- **left_hand**: 16-position array (16th note grid)
- **velocities**: Note volumes (0-127)
- **durations**: Note lengths in ticks
- **melody_type**: "chord", "melody", or "solo"

### Pattern Values

| Value | Right Hand | Left Hand |
|-------|------------|-----------|
| `0` | Rest | Rest |
| `1` | Chord | Chord |
| `2` | N/A | Bass note |
| `3` | Melody note | N/A |
| `4` | Solo note | N/A |

## 🎵 Musical Features

### Right Hand Variations

1. **Chord Comping** (`melody_type: "chord"`)
   - Uses `right_hand` voicings
   - Traditional jazz chord hits
   - Pattern value: `1`

2. **Melodic Lines** (`melody_type: "melody"`)
   - Uses `right_hand_melody` arrays
   - 8-note melodic phrases
   - Pattern value: `3`

3. **Solo Passages** (`melody_type: "solo"`)
   - Uses `right_hand_solo` arrays
   - 16-note bebop runs
   - Pattern value: `4`

### Left Hand Structure

- **Bass Line**: Root notes on strong beats
  - Pattern value: `2`
  - Uses `left_hand.bass` note
  - Typically 8th note duration

- **Chord Support**: 3-note voicings
  - Pattern value: `1`
  - Uses `left_hand.chord` array
  - Longer durations for harmonic support

### Timing and Velocity

- **16th Note Grid**: Each measure = 16 positions
- **Flexible Durations**: Per-pattern timing control
- **Dynamic Levels**: Velocity ranges create musical expression
- **Proper Voice Leading**: Smooth transitions between chords

## 🔧 API Reference

### ConfigurableMIDIGenerator Class

```python
generator = ConfigurableMIDIGenerator()
```

#### Methods

**`load_configuration(config_path_or_dict)`**
- Load from JSON file path or dictionary
- Validates required sections
- Raises ValueError for invalid configs

**`create_composition(output_filename=None)`**
- Generate MIDI composition
- Returns output file path
- Auto-creates `./output/` directory

#### Internal Methods

**`_generate_events()`**
- Convert configuration to MIDI events
- Handles all timing calculations
- Returns sorted event list

**`_generate_measure_events(chord_symbol, patterns, start_time)`**
- Generate events for single measure
- Applies patterns to chord voicings
- Handles melody type switching

**`_events_to_midi(events)`**
- Convert events to MIDI messages
- Calculates delta times
- Writes to MIDI track

### Convenience Functions

**`create_midi_from_config(config_file)`**
- One-line composition generation
- Auto-checks `./config/` folder
- Returns output file path

## 🔍 Analysis Tools

### utils/midi_analyzer.py

```bash
python utils/midi_analyzer.py <filename.mid>
```

**Features:**
- Track information and metadata
- Note range analysis (playability check)
- Event counting and statistics
- Tempo and time signature detection
- Auto-checks `./output/` folder

**Output Example:**
```
🎼 MIDI FILE ANALYSIS: output/jazz_variations.mid
==================================================
📁 File: output/jazz_variations.mid
🎵 Tracks: 1
⏱️  Ticks per beat: 480

🎵 TRACK 1
--------------------
📋 Track Name: Professional Jazz Piano with Melodic Variations
🎼 Tempo: 125.0 BPM
🎵 Time Signature: 4/4

   Right Hand (Channel 0):
     🎼 Range: G3 to A#5
     📊 Notes: 344
     ✅ Good treble range

   Left Hand (Channel 1):
     🎼 Range: C3 to A4
     📊 Notes: 560
     ✅ Good bass range
```

### utils/midi_inspector.py

More detailed analysis for debugging and development.

## 🎯 Usage Examples

### Basic Generation

```python
from midi import ConfigurableMIDIGenerator

# Method 1: Direct usage
generator = ConfigurableMIDIGenerator()
generator.load_configuration('config/jazz_config.json')
output_file = generator.create_composition()

# Method 2: Convenience function
output_file = create_midi_from_config('jazz_config.json')
```

### Command Line

```bash
# Generate composition
python midi.py jazz_config.json

# List available configs
python midi.py

# Analyze output
python utils/midi_analyzer.py jazz_variations.mid
```

### Custom Configuration

```python
config = {
    "metadata": {
        "title": "My Song",
        "tempo": 120,
        "output_filename": "my_song.mid"
    },
    "chord_progressions": {
        "structure": ["verse"],
        "sections": {
            "verse": ["C", "Am", "F", "G"]
        }
    },
    # ... rest of config
}

generator = ConfigurableMIDIGenerator()
generator.load_configuration(config)
generator.create_composition()
```

## 🎨 Creating New Configurations

### 1. Define Structure
Start with basic metadata and chord progression:

```json
{
  "metadata": {
    "title": "New Song",
    "tempo": 120,
    "output_filename": "new_song.mid"
  },
  "chord_progressions": {
    "structure": ["verse", "chorus"],
    "sections": {
      "verse": ["C", "Am", "F", "G"],
      "chorus": ["F", "C", "G", "Am"]
    }
  }
}
```

### 2. Add Voicings
Define how each chord should be played:

```json
"chord_voicings": {
  "C": {
    "right_hand": [60, 64, 67],
    "left_hand": {
      "bass": 36,
      "chord": [43, 47, 52]
    }
  }
}
```

### 3. Create Patterns
Define rhythmic patterns for each section:

```json
"patterns": {
  "verse": {
    "right_hand": [1, 0, 1, 0, 1, 0, 1, 0],
    "left_hand": [2, 0, 1, 0, 2, 0, 1, 0],
    "rh_velocity": 80,
    "lh_velocity": 70,
    "melody_type": "chord"
  }
}
```

## 🐛 Troubleshooting

### Common Issues

**Config file not found:**
- Check file is in `./config/` folder
- Verify JSON syntax (no trailing commas)
- Use `python midi.py` to list available configs

**Invalid JSON syntax:**
- Validate JSON with online checker
- Common errors: trailing commas, missing quotes
- Check bracket/brace matching

**MIDI sounds wrong:**
- Verify note ranges (C3-C7 for piano)
- Check velocity values (30-127 recommended)
- Ensure proper chord voicings

**Pattern issues:**
- Patterns must be 16 values long
- Use only valid pattern values (0-4)
- Check melody_type matches pattern content

### Debugging

Use the analyzer for verification:

```bash
python utils/midi_analyzer.py output/your_file.mid
```

Check note ranges, count, and playability.

## 🎼 MIDI Note Numbers

### Piano Range Reference

| Note | Octave | MIDI # | Usage |
|------|--------|--------|-------|
| C3 | 3 | 48 | Bass notes |
| C4 | 4 | 60 | Middle C |
| C5 | 5 | 72 | Melody range |
| C6 | 6 | 84 | High notes |

### Recommended Ranges

- **Left Hand Bass**: C2 (36) to C4 (60)
- **Left Hand Chords**: C3 (48) to C5 (72)
- **Right Hand**: C4 (60) to C7 (96)

## 🚀 Advanced Features

### Dynamic Patterns

Different sections can have different complexity:

```json
"patterns": {
  "intro": {
    "right_hand": [1, 0, 0, 1, 0, 1, 0, 0],
    "melody_type": "chord"
  },
  "solo": {
    "right_hand": [4, 4, 4, 4, 4, 4, 4, 4],
    "melody_type": "solo"
  }
}
```

### Multiple Voicing Arrays

Support for variation within sections:

```json
"right_hand_melody": [
  [72, 75, 77, 75],  // Phrase 1
  [77, 75, 72, 70]   // Phrase 2
]
```

### Complex Left Hand Patterns

Sophisticated bass lines:

```json
"left_hand": [2, 0, 1, 1, 1, 0, 0, 0, 2, 0, 1, 1, 1, 0, 0, 0]
```
- `2` = Root note (8th duration)
- `1` = Chord triad (longer duration)

## 📝 Contributing

When creating new configurations:

1. **Test thoroughly** with analyzer
2. **Document musical intent** in comments
3. **Use consistent naming** conventions
4. **Verify playability** on actual piano
5. **Include usage examples**

---

*For jazz-specific features and examples, see [JAZZ_VARIATIONS_GUIDE.md](JAZZ_VARIATIONS_GUIDE.md)*
      "rh_velocity": 80,
      "lh_velocity": 70
    }
  }
}
```

## Pattern System

**Right Hand Patterns:**
- `0` = Rest
- `1` = Play chord notes

**Left Hand Patterns:**
- `0` = Rest  
- `1` = Play chord tones
- `2` = Play bass note

Each pattern has 16 positions (16th note grid for one measure).

## Piano Range Guidelines

**Proper Piano Ranges:**
- Right Hand: C4 to C7 (treble clef)
- Left Hand: C2 to C5 (bass clef)

**MIDI Note Numbers:**
- C4 = 60 (Middle C)
- C3 = 48 (Good bass starting point)
- C5 = 72 (Good treble upper limit for intermediate players)

## Example Configurations

### 1. Professional Jazz (`professional_jazz_config.json`)
- 20 bars, 125 BPM
- Complex harmony with shell voicings
- Progressive build-up through sections

### 2. Simple Ballad (`simple_ballad_config.json`) 
- 8 bars, 120 BPM
- Basic chord progression
- Gentle rhythmic patterns

## Usage Examples

```bash
# Generate from configuration
python midi.py professional_jazz_config.json

# Analyze generated file
python midi_analyzer.py professional_jazz_config.mid

# Analyze multiple files
python midi_analyzer.py *.mid
```

## File Structure

```
Music/
├── midi.py                          # Main generator
├── midi_analyzer.py                 # Analysis tool
├── professional_jazz_config.json   # Complex jazz example
├── simple_ballad_config.json       # Simple ballad example
├── professional_jazz_config.mid    # Generated output
└── simple_ballad.mid               # Generated output
```

## Benefits

✅ **No more script proliferation** - One generator for all compositions
✅ **Easy iteration** - Just edit JSON, no Python code changes
✅ **Reusable configurations** - Share and modify existing arrangements
✅ **Proper piano ranges** - Built-in validation for playability
✅ **Generic analysis** - One analyzer works for all generated files

## Creating New Compositions

1. Copy an existing config file
2. Modify chord progressions, voicings, and patterns
3. Run `python midi.py your_config.json`
4. Analyze with `python midi_analyzer.py your_output.mid`

## Advanced Features

- **Shell voicings** - Professional jazz piano technique
- **Voice leading** - Smooth chord progressions
- **Dynamic builds** - Different velocities per section
- **Flexible sections** - Any number of musical sections
- **Pattern variations** - Different rhythms per section
