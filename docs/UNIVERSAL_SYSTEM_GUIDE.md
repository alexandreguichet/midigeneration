# Universal MIDI Generator - Complete Data-Driven System

## Overview

The Universal MIDI Generator is a completely data-driven music composition system that separates all musical logic from code. Every aspect of the generated music is configurable through JSON files, making it scalable to any instrument, genre, or musical style.

## Key Features

- ✅ **100% Data-Driven**: No hardcoded musical elements in the code
- ✅ **Any Instrument Support**: Piano, strings, synths, drums, custom instruments
- ✅ **Any Genre**: Jazz, classical, electronic, pop, world music, etc.
- ✅ **Scalable Patterns**: From simple melodies to complex polyrhythms
- ✅ **Algorithmic Generation**: Walking bass, arpeggios, scale patterns
- ✅ **Advanced Timing**: Swing, humanization, custom timing offsets
- ✅ **Multiple Voicings**: Close, open, spread voicings for any chord
- ✅ **Song Structure**: Verses, choruses, bridges, custom sections
- ✅ **Dynamic Expression**: Crescendos, accents, velocity curves

## System Architecture

### 1. Configuration Structure

```
config/
├── universal_template.json      # Master template with all features
├── jazz_piano_trio.json        # Jazz ensemble example
├── classical_string_quartet.json # Classical music example
├── progressive_house.json      # Electronic music example
└── [your_custom_config].json   # Your configurations
```

### 2. Code Structure

```
src/
└── universal_midi_generator.py  # Single generator handles all styles
```

## Configuration Sections

### Metadata
Controls global song parameters:
```json
{
  "metadata": {
    "title": "Your Song Title",
    "tempo": 120,
    "time_signature": [4, 4],
    "ticks_per_beat": 480,
    "swing_ratio": 0.67,
    "key_signature": "C",
    "output_filename": "output/your_song.mid"
  }
}
```

### Instruments
Define any number of instruments with their properties:
```json
{
  "instruments": {
    "piano_right": {
      "name": "Piano Right Hand",
      "midi_channel": 0,
      "program_number": 0,
      "default_velocity": 85,
      "velocity_range": [60, 110],
      "note_range": [60, 96]
    }
  }
}
```

### Song Structure
Create complex song forms:
```json
{
  "song_structure": {
    "sections": ["intro", "verse", "chorus", "bridge", "outro"],
    "section_definitions": {
      "verse": {
        "length_bars": 8,
        "chord_progression": ["C", "Am", "F", "G"],
        "pattern_assignment": {
          "piano_right": "melody_pattern",
          "piano_left": "bass_pattern"
        }
      }
    }
  }
}
```

### Chord Library
Define chords with multiple voicings and scales:
```json
{
  "chord_library": {
    "C": {
      "root_note": 60,
      "chord_tones": [0, 4, 7],
      "voicings": {
        "close": [60, 64, 67],
        "open": [60, 67, 72],
        "spread": [48, 64, 67, 72]
      },
      "scales": {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "pentatonic": [0, 2, 4, 7, 9]
      }
    }
  }
}
```

### Pattern Library
Create rhythmic and melodic patterns:
```json
{
  "pattern_library": {
    "melody_pattern": {
      "instrument": "piano_right",
      "note_pattern": [1, 2, 3, 2, 1, 0, 4, 3],
      "note_source": "scale_major",
      "velocity_pattern": [85, 80, 90, 80, 75, 0, 95, 85],
      "duration_pattern": [120, 120, 240, 120, 240, 0, 240, 360],
      "timing_offset": 0,
      "melodic_direction": "ascending",
      "scale_start_degree": 1
    }
  }
}
```

## Note Sources

The system supports various note sources:

### Fixed Sources
- `bass_note`: Use chord's bass note
- `chord_voicing_[type]`: Use specific voicing (close, open, spread, etc.)

### Scale-Based Sources
- `scale_major`: Major scale patterns
- `scale_pentatonic`: Pentatonic scale patterns
- `scale_mixolydian`: Mixolydian mode
- `scale_altered`: Altered scale for jazz

### Algorithmic Sources
- `arpeggio_up`: Ascending arpeggio
- `arpeggio_down`: Descending arpeggio
- `walking_pattern`: Walking bass lines with chromatic approach
- `drum_note`: Single drum hits

## Pattern Features

### Rhythmic Patterns
- **note_pattern**: 16-step pattern (0=rest, 1-8=note values)
- **velocity_pattern**: Dynamic expression for each step
- **duration_pattern**: Note lengths in MIDI ticks
- **timing_offset**: Micro-timing adjustments

### Melodic Control
- **melodic_direction**: ascending, descending, mixed, contrary
- **scale_start_degree**: Starting point in the scale
- **arpeggio_octaves**: Range for arpeggio patterns

### Specialized Algorithms
- **walking_algorithm**: chromatic_approach, diatonic
- **step_size_range**: Control interval sizes
- **approach_distance**: Chromatic approach note distance

## Global Modifiers

### Swing Timing
```json
{
  "swing_timing": {
    "enabled": true,
    "swing_ratio": 0.67,
    "apply_to_subdivisions": ["eighth", "sixteenth"]
  }
}
```

### Humanization
```json
{
  "humanization": {
    "timing_variance": 5,
    "velocity_variance": 8,
    "enabled": true
  }
}
```

### Dynamics
```json
{
  "dynamics": {
    "crescendo_sections": ["bridge"],
    "diminuendo_sections": ["outro"],
    "accent_beats": [1, 3]
  }
}
```

## Usage Examples

### 1. Generate Jazz Piano Trio
```bash
python src/universal_midi_generator.py config/jazz_piano_trio.json
```

### 2. Generate Classical String Quartet
```bash
python src/universal_midi_generator.py config/classical_string_quartet.json
```

### 3. Generate Electronic Dance Music
```bash
python src/universal_midi_generator.py config/progressive_house.json
```

## Creating Custom Configurations

### 1. Start with Template
Copy `universal_template.json` and modify for your needs.

### 2. Define Your Instruments
Set up MIDI channels, program numbers, and ranges.

### 3. Create Chord Progressions
Add chords with appropriate voicings for your style.

### 4. Design Patterns
Create rhythmic and melodic patterns for each instrument.

### 5. Structure Your Song
Define sections and assign patterns to instruments.

## Advanced Features

### Custom Instruments
Support for any MIDI instrument:
```json
{
  "custom_synth": {
    "name": "Custom Lead Synthesizer",
    "midi_channel": 5,
    "program_number": 81,
    "note_range": [48, 84],
    "default_velocity": 100
  }
}
```

### Complex Time Signatures
```json
{
  "time_signature": [7, 8],  # 7/8 time
  "ticks_per_beat": 480
}
```

### Extended Harmonies
```json
{
  "Cmaj13": {
    "chord_tones": [0, 4, 7, 11, 14, 17, 21],
    "extensions": [24, 28, 31],
    "voicings": {
      "modern": [60, 71, 76, 83, 86]
    }
  }
}
```

### Polyrhythmic Patterns
```json
{
  "polyrhythm_3_against_2": {
    "note_pattern": [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    "subdivision_ratio": [3, 2]
  }
}
```

## Performance Tips

1. **Optimization**: Limit `note_range` for better instrument realism
2. **Humanization**: Use moderate values (3-8) for natural feel
3. **Velocity**: Layer instruments with different velocity ranges
4. **Timing**: Small timing offsets (5-30 ticks) create ensemble feel
5. **Structure**: Use pattern variations to avoid repetition

## Troubleshooting

### Common Issues

1. **No sound generated**: Check instrument `note_range` and `note_pattern`
2. **Timing problems**: Verify `ticks_per_beat` and `duration_pattern`
3. **Wrong notes**: Check `chord_library` and `note_source` mappings
4. **Channel conflicts**: Ensure unique `midi_channel` per instrument

### Validation

The system validates:
- JSON syntax and structure
- Required configuration sections
- Instrument channel assignments
- Pattern array lengths

## Extension Examples

### World Music Scale
```json
{
  "scales": {
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "blues": [0, 3, 5, 6, 7, 10],
    "arabic_maqam": [0, 1, 4, 5, 7, 8, 11]
  }
}
```

### Drum Patterns
```json
{
  "kick_drum": {
    "midi_channel": 9,
    "note_range": [36, 36],
    "patterns": {
      "four_on_floor": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    }
  }
}
```

### Microrhythms
```json
{
  "afro_cuban_clave": {
    "note_pattern": [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    "timing_offset": [0, 0, 0, 5, 0, 0, -3, 0, 0, 0, 8, 0, -5, 0, 0, 0]
  }
}
```

## Conclusion

The Universal MIDI Generator provides a completely flexible, data-driven approach to algorithmic composition. By separating musical logic from code, it enables rapid prototyping of any musical style while maintaining the power to create sophisticated, nuanced compositions.

The system scales from simple melodies to complex orchestral arrangements, making it suitable for:
- Music education and theory exploration
- Rapid prototyping of musical ideas
- Algorithmic composition research
- Game music generation
- Backing track creation
- Style analysis and reproduction

Every aspect is configurable, ensuring the system can adapt to any musical requirement without code modifications.
