#!/usr/bin/env python3
"""
Universal MIDI Generator - Data-Driven Music Composition
Generates MIDI files from JSON configuration with complete separation of musical logic from code.
"""

import json
import sys
from pathlib import Path
import mido
import random
import copy
from typing import Dict, List, Any, Tuple, Optional


class UniversalMIDIGenerator:
    """
    Completely data-driven MIDI generator that reads all musical information from JSON configuration.
    No hardcoded musical elements - everything is configurable.
    """

    def __init__(self, config_path: str):
        """Initialize generator with configuration file."""
        self.config = self.load_config(config_path)
        self.midi_file = mido.MidiFile(ticks_per_beat=self.config['metadata']['ticks_per_beat'])
        self.tracks = {}
        self.current_chord_index = 0
        self.current_section = None
        
        # Initialize tracks for each instrument
        self._initialize_tracks()

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Load and validate configuration file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✓ Loaded configuration: {config['metadata']['title']}")
            return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration: {e}")

    def _initialize_tracks(self):
        """Create MIDI tracks for each instrument."""
        for instrument_id, instrument_config in self.config['instruments'].items():
            track = mido.MidiTrack()
            
            # Set instrument program
            track.append(mido.Message(
                'program_change',
                channel=instrument_config['midi_channel'],
                program=instrument_config['program_number'],
                time=0
            ))
            
            self.tracks[instrument_id] = track
            self.midi_file.tracks.append(track)
            print(f"✓ Initialized track for {instrument_config['name']} (Channel {instrument_config['midi_channel']})")

    def generate_song(self):
        """Generate complete song based on configuration structure."""
        print(f"\n🎵 Generating {self.config['metadata']['title']}...")
        
        # Process each section in the song structure
        for section_name in self.config['song_structure']['sections']:
            self._generate_section(section_name)
        
        # Add final timing to all tracks
        self._finalize_tracks()
        
        print(f"✓ Song generation complete!")

    def _generate_section(self, section_name: str):
        """Generate a specific section of the song."""
        section_config = self.config['song_structure']['section_definitions'][section_name]
        self.current_section = section_name
        
        print(f"  Generating section: {section_name} ({section_config['length_bars']} bars)")
        
        # Generate each bar in the section
        for bar_index in range(section_config['length_bars']):
            chord_name = section_config['chord_progression'][bar_index % len(section_config['chord_progression'])]
            self._generate_bar(section_config, chord_name, bar_index)

    def _generate_bar(self, section_config: Dict, chord_name: str, bar_index: int):
        """Generate one bar of music for all instruments."""
        current_chord = self.config['chord_library'][chord_name]
        
        # Generate patterns for each instrument in this section
        for instrument_id, pattern_name in section_config['pattern_assignment'].items():
            self._generate_instrument_pattern(instrument_id, pattern_name, current_chord, bar_index)

    def _generate_instrument_pattern(self, instrument_id: str, pattern_name: str, current_chord: Dict, bar_index: int):
        """Generate pattern for a specific instrument."""
        pattern = self.config['pattern_library'][pattern_name]
        instrument = self.config['instruments'][instrument_id]
        track = self.tracks[instrument_id]
        
        # Get the note pattern and associated data
        note_pattern = pattern['note_pattern']
        velocity_pattern = pattern['velocity_pattern']
        duration_pattern = pattern['duration_pattern']
        
        # Calculate timing for this bar
        bar_start_time = bar_index * self.config['metadata']['ticks_per_beat'] * self.config['metadata']['time_signature'][0]
        subdivision_length = self.config['metadata']['ticks_per_beat'] // 4  # 16th note subdivisions
        
        # Process each step in the pattern
        for step_index, note_value in enumerate(note_pattern):
            if note_value == 0:  # Rest
                continue
                
            step_time = bar_start_time + (step_index * subdivision_length)
            velocity = velocity_pattern[step_index] if step_index < len(velocity_pattern) else instrument['default_velocity']
            duration = duration_pattern[step_index] if step_index < len(duration_pattern) else subdivision_length
            
            # Apply swing timing if enabled
            if self._should_apply_swing(step_index):
                step_time += self._calculate_swing_offset(subdivision_length)
            
            # Apply humanization
            if self.config.get('global_modifiers', {}).get('humanization', {}).get('enabled', False):
                step_time, velocity = self._apply_humanization(step_time, velocity)
            
            # Get the actual notes to play
            notes = self._resolve_note_source(pattern['note_source'], current_chord, note_value, step_index, pattern)
            
            # Add notes to track
            for note in notes:
                if self._is_note_in_range(note, instrument):
                    self._add_note_to_track(track, note, velocity, duration, step_time, instrument['midi_channel'])

    def _resolve_note_source(self, note_source: str, current_chord: Dict, note_value: int, step_index: int, pattern: Dict) -> List[int]:
        """Resolve note source to actual MIDI note numbers."""
        
        if note_source == "bass_note":
            return [current_chord['bass_note']]
        
        elif note_source == "drum_note":
            # For drum patterns, use the instrument's note range
            instrument_id = pattern['instrument']
            instrument = self.config['instruments'][instrument_id]
            note_range = instrument['note_range']
            return [note_range[0]]  # Use the first note in the range
        
        elif note_source.startswith("chord_voicing_"):
            voicing_type = note_source.replace("chord_voicing_", "")
            return current_chord['voicings'][voicing_type]
        
        elif note_source.startswith("scale_"):
            scale_type = note_source.replace("scale_", "")
            return self._generate_scale_notes(current_chord, scale_type, note_value, pattern)
        
        elif note_source.startswith("arpeggio_"):
            direction = note_source.replace("arpeggio_", "")
            return self._generate_arpeggio_notes(current_chord, direction, note_value, step_index, pattern)
        
        elif note_source == "walking_pattern":
            return self._generate_walking_bass(current_chord, note_value, step_index, pattern)
        
        else:
            # Default to chord tones
            root = current_chord['root_note']
            return [root + interval for interval in current_chord['chord_tones']]

    def _generate_scale_notes(self, current_chord: Dict, scale_type: str, note_value: int, pattern: Dict) -> List[int]:
        """Generate notes from specified scale."""
        if scale_type not in current_chord['scales']:
            scale_type = list(current_chord['scales'].keys())[0]  # Use first available scale
        
        scale = current_chord['scales'][scale_type]
        root = current_chord['root_note']
        
        # Get starting degree and direction from pattern
        start_degree = pattern.get('scale_start_degree', 1) - 1
        direction = pattern.get('melodic_direction', 'ascending')
        
        # Calculate note based on value and direction
        if direction == 'ascending':
            degree_index = (start_degree + note_value - 1) % len(scale)
        else:
            degree_index = (start_degree - note_value + 1) % len(scale)
        
        note = root + scale[degree_index]
        return [note]

    def _generate_arpeggio_notes(self, current_chord: Dict, direction: str, note_value: int, step_index: int, pattern: Dict) -> List[int]:
        """Generate arpeggio notes."""
        chord_tones = current_chord['chord_tones']
        root = current_chord['root_note']
        octaves = pattern.get('arpeggio_octaves', 1)
        
        # Build extended arpeggio across octaves
        extended_arpeggio = []
        for octave in range(octaves + 1):
            for interval in chord_tones:
                extended_arpeggio.append(root + interval + (octave * 12))
        
        if direction == 'down':
            extended_arpeggio.reverse()
        
        # Select note based on step
        note_index = (step_index * note_value) % len(extended_arpeggio)
        return [extended_arpeggio[note_index]]

    def _generate_walking_bass(self, current_chord: Dict, note_value: int, step_index: int, pattern: Dict) -> List[int]:
        """Generate walking bass line."""
        algorithm = pattern.get('walking_algorithm', 'diatonic')
        bass_note = current_chord['bass_note']
        
        if algorithm == 'chromatic_approach':
            # Generate chromatic approach to next chord (simplified)
            offset = (step_index % 4) - 2  # -2, -1, 0, 1
            return [bass_note + offset]
        
        elif algorithm == 'diatonic':
            # Use scale steps
            if 'scales' in current_chord:
                scale = list(current_chord['scales'].values())[0]
                step_size = pattern.get('step_size_range', [1, 3])[0]
                scale_note = bass_note + scale[step_index % len(scale)]
                return [scale_note]
        
        # Default to bass note
        return [bass_note]

    def _should_apply_swing(self, step_index: int) -> bool:
        """Check if swing timing should be applied to this step."""
        swing_config = self.config.get('global_modifiers', {}).get('swing_timing', {})
        
        if not swing_config.get('enabled', False):
            return False
        
        # Apply swing to off-beats (assuming 16th note subdivisions)
        return step_index % 2 == 1

    def _calculate_swing_offset(self, subdivision_length: int) -> int:
        """Calculate swing timing offset."""
        swing_ratio = self.config.get('global_modifiers', {}).get('swing_timing', {}).get('swing_ratio', 0.67)
        swing_offset = int(subdivision_length * (swing_ratio - 0.5))
        return swing_offset

    def _apply_humanization(self, timing: int, velocity: int) -> Tuple[int, int]:
        """Apply humanization to timing and velocity."""
        humanization = self.config.get('global_modifiers', {}).get('humanization', {})
        
        timing_variance = humanization.get('timing_variance', 5)
        velocity_variance = humanization.get('velocity_variance', 8)
        
        timing += random.randint(-timing_variance, timing_variance)
        velocity += random.randint(-velocity_variance, velocity_variance)
        velocity = max(1, min(127, velocity))  # Keep velocity in valid range
        
        return timing, velocity

    def _is_note_in_range(self, note: int, instrument: Dict) -> bool:
        """Check if note is within instrument's range."""
        note_range = instrument.get('note_range', [0, 127])
        return note_range[0] <= note <= note_range[1]

    def _add_note_to_track(self, track: mido.MidiTrack, note: int, velocity: int, duration: int, 
                          start_time: int, channel: int):
        """Add a note to the MIDI track with proper timing."""
        
        # Calculate time delta from last event
        current_track_time = sum(msg.time for msg in track)
        time_delta = max(0, start_time - current_track_time)
        
        # Note on
        track.append(mido.Message(
            'note_on',
            channel=channel,
            note=note,
            velocity=velocity,
            time=time_delta
        ))
        
        # Note off
        track.append(mido.Message(
            'note_off',
            channel=channel,
            note=note,
            velocity=0,
            time=duration
        ))

    def _finalize_tracks(self):
        """Add final timing adjustments to all tracks."""
        # Ensure all tracks end at the same time
        max_length = 0
        for track in self.tracks.values():
            track_length = sum(msg.time for msg in track)
            max_length = max(max_length, track_length)
        
        # Pad shorter tracks
        for track in self.tracks.values():
            track_length = sum(msg.time for msg in track)
            if track_length < max_length:
                track.append(mido.Message('note_off', channel=0, note=60, velocity=0, time=max_length - track_length))

    def save_midi_file(self, output_path: Optional[str] = None):
        """Save the generated MIDI file."""
        if output_path is None:
            output_path = self.config['metadata']['output_filename']
        
        # Ensure output directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.midi_file.save(output_path)
        file_size = Path(output_path).stat().st_size
        print(f"✓ MIDI file saved: {output_path} ({file_size:,} bytes)")
        
        return output_path

    def get_generation_stats(self) -> Dict[str, Any]:
        """Get statistics about the generated music."""
        total_notes = 0
        track_stats = {}
        
        for instrument_id, track in self.tracks.items():
            note_count = sum(1 for msg in track if msg.type == 'note_on')
            track_stats[instrument_id] = {
                'note_count': note_count,
                'instrument_name': self.config['instruments'][instrument_id]['name']
            }
            total_notes += note_count
        
        return {
            'total_notes': total_notes,
            'total_tracks': len(self.tracks),
            'title': self.config['metadata']['title'],
            'tempo': self.config['metadata']['tempo'],
            'track_stats': track_stats
        }


def main():
    """Main entry point for the universal MIDI generator."""
    if len(sys.argv) != 2:
        print("Usage: python universal_midi_generator.py <config_file.json>")
        print("\nExample configurations available in config/ directory:")
        config_dir = Path("config")
        if config_dir.exists():
            for config_file in config_dir.glob("*.json"):
                print(f"  - {config_file}")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        # Generate music
        generator = UniversalMIDIGenerator(config_file)
        generator.generate_song()
        output_file = generator.save_midi_file()
        
        # Display generation statistics
        stats = generator.get_generation_stats()
        print(f"\n📊 Generation Statistics:")
        print(f"   Title: {stats['title']}")
        print(f"   Total Notes: {stats['total_notes']}")
        print(f"   Total Tracks: {stats['total_tracks']}")
        print(f"   Tempo: {stats['tempo']} BPM")
        
        print(f"\n🎹 Track Details:")
        for instrument_id, track_stats in stats['track_stats'].items():
            print(f"   {track_stats['instrument_name']}: {track_stats['note_count']} notes")
        
        print(f"\n✅ Universal MIDI generation complete!")
        return output_file
        
    except Exception as e:
        print(f"❌ Error generating MIDI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
