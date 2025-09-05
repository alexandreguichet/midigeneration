import json
import os
from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from pathlib import Path

class ConfigurableMIDIGenerator:
    """
    Generic MIDI generator that creates compositions from JSON configuration files.
    Supports flexible chord progressions, voicings, patterns, and arrangement styles.
    """
    
    def __init__(self):
        self.mid = None
        self.track = None
        self.config = None
        
    def load_configuration(self, config_path_or_dict):
        """Load configuration from JSON file or dictionary"""
        if isinstance(config_path_or_dict, (str, Path)):
            with open(config_path_or_dict, 'r') as f:
                self.config = json.load(f)
        elif isinstance(config_path_or_dict, dict):
            self.config = config_path_or_dict
        else:
            raise ValueError("Configuration must be a file path or dictionary")
        
        # Validate required sections
        required_sections = ['metadata', 'chord_progressions', 'chord_voicings', 'patterns']
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
    
    def create_composition(self, output_filename=None):
        """Generate MIDI composition from loaded configuration"""
        if not self.config:
            raise ValueError("No configuration loaded. Call load_configuration() first.")
        
        # Initialize MIDI file
        metadata = self.config['metadata']
        self.mid = MidiFile(ticks_per_beat=metadata.get('ticks_per_beat', 480))
        self.track = MidiTrack()
        self.mid.tracks.append(self.track)
        
        # Set tempo and time signature
        tempo = bpm2tempo(metadata.get('tempo', 120))
        self.track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        self.track.append(MetaMessage('time_signature', 
                                    numerator=metadata.get('time_signature', [4, 4])[0],
                                    denominator=metadata.get('time_signature', [4, 4])[1],
                                    clocks_per_click=24, 
                                    notated_32nd_notes_per_beat=8, time=0))
        self.track.append(MetaMessage('track_name', name=metadata.get('title', 'Generated Composition'), time=0))
        
        # Generate composition
        events = self._generate_events()
        self._events_to_midi(events)
        
        # Save file
        if not output_filename:
            output_filename = metadata.get('output_filename', 'generated_composition.mid')
        
        # Create output directory
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        # Ensure the filename is in the output directory
        output_path = output_dir / Path(output_filename).name
        
        self.mid.save(str(output_path))
        print(f"🎼 Generated '{output_path}'")
        print(f"📊 {metadata.get('title', 'Composition')} - {metadata.get('tempo', 120)} BPM")
        return str(output_path)
    
    def _generate_events(self):
        """Generate all musical events from configuration"""
        events = []
        ticks_per_beat = self.config['metadata'].get('ticks_per_beat', 480)
        beats_per_measure = self.config['metadata'].get('time_signature', [4, 4])[0]
        measure_length = ticks_per_beat * beats_per_measure
        
        # Get sections and their chord progressions
        sections = self.config['chord_progressions']['sections']
        structure = self.config['chord_progressions'].get('structure', list(sections.keys()))
        
        measure_num = 0
        for section_name in structure:
            section_chords = sections[section_name]
            section_patterns = self.config['patterns'].get(section_name, self.config['patterns']['default'])
            
            print(f"\n🎵 Section: {section_name}")
            
            for chord_name in section_chords:
                chord_voicing = self.config['chord_voicings'][chord_name]
                measure_start_time = measure_num * measure_length
                
                print(f"  Bar {measure_num + 1}: {chord_name}")
                
                # Generate events for this measure
                measure_events = self._generate_measure_events(
                    chord_voicing, section_patterns, measure_start_time, ticks_per_beat
                )
                events.extend(measure_events)
                measure_num += 1
        
        return events

    
    def _generate_measure_events(self, chord_voicing, patterns, start_time, ticks_per_beat):
        """Generate events for a single measure with melody variations"""
        events = []
        sixteenth_note = ticks_per_beat // 4
        
        # Get patterns for this measure
        rh_pattern = patterns.get('right_hand', [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0])
        lh_pattern = patterns.get('left_hand', [2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0])
        melody_type = patterns.get('melody_type', 'chord')
        
        # Right hand events with melody variations
        if 'right_hand' in chord_voicing:
            melody_idx = 0
            solo_idx = 0
            
            for i, hit in enumerate(rh_pattern):
                if hit:
                    current_time = start_time + (i * sixteenth_note)
                    duration = patterns.get('rh_duration', ticks_per_beat // 2)
                    velocity = patterns.get('rh_velocity', 80)
                    
                    if hit == 1:  # Chord comping
                        notes = chord_voicing['right_hand']
                    elif hit == 3 and melody_type == 'melody':  # Melodic line
                        if 'right_hand_melody' in chord_voicing:
                            melody_notes = chord_voicing['right_hand_melody']
                            notes = [melody_notes[melody_idx % len(melody_notes)]]
                            melody_idx += 1
                        else:
                            notes = chord_voicing['right_hand']
                    elif hit == 4 and melody_type == 'solo':  # 16th note solo
                        if 'right_hand_solo' in chord_voicing:
                            solo_notes = chord_voicing['right_hand_solo']
                            notes = [solo_notes[solo_idx % len(solo_notes)]]
                            solo_idx += 1
                        else:
                            notes = chord_voicing['right_hand']
                    else:
                        notes = chord_voicing['right_hand']
                    
                    if isinstance(notes[0], list):  # Multiple note sets
                        notes = notes[i % len(notes)]
                    
                    for note in notes:
                        events.append(('note_on', note, current_time, 0, velocity))
                        events.append(('note_off', note, current_time + duration, 0, velocity))
        
        # Left hand events
        if 'left_hand' in chord_voicing:
            for i, pattern_type in enumerate(lh_pattern):
                if pattern_type > 0:
                    current_time = start_time + (i * sixteenth_note)
                    velocity = patterns.get('lh_velocity', 70)
                    
                    if pattern_type == 1:  # Chord
                        notes = chord_voicing['left_hand'].get('chord', [])
                        duration = patterns.get('lh_chord_duration', ticks_per_beat // 2)
                    elif pattern_type == 2:  # Bass
                        notes = [chord_voicing['left_hand'].get('bass', 48)]
                        duration = patterns.get('lh_bass_duration', ticks_per_beat)
                    
                    for note in notes:
                        events.append(('note_on', note, current_time, 1, velocity))
                        events.append(('note_off', note, current_time + duration, 1, velocity))
        
        return events
    
    def _events_to_midi(self, events):
        """Convert events to MIDI messages"""
        events.sort(key=lambda x: x[2])  # Sort by time
        prev_time = 0
        
        for event_type, note, abs_time, channel, velocity in events:
            delta_time = abs_time - prev_time
            
            if event_type == 'note_on':
                self.track.append(Message('note_on', note=note, velocity=velocity, 
                                        channel=channel, time=delta_time))
            elif event_type == 'note_off':
                self.track.append(Message('note_off', note=note, velocity=velocity, 
                                        channel=channel, time=delta_time))
            
            prev_time = abs_time

def create_midi_from_config(config_file):
    """Convenience function to create MIDI from configuration file"""
    # Check if file exists, if not try the config folder
    config_path = Path(config_file)
    if not config_path.exists():
        config_folder_path = Path('config') / config_path.name
        if config_folder_path.exists():
            config_path = config_folder_path
        else:
            print(f"❌ Config file not found: {config_file}")
            print(f"❌ Also checked: {config_folder_path}")
            return None
    
    generator = ConfigurableMIDIGenerator()
    generator.load_configuration(str(config_path))
    return generator.create_composition()

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        result = create_midi_from_config(config_file)
        if result is None:
            print("\n💡 Available configs:")
            config_dir = Path('config')
            if config_dir.exists():
                for config in config_dir.glob('*.json'):
                    print(f"   - {config.name}")
            print("\n🔍 Analysis tools:")
            print("   python utils/midi_analyzer.py <filename.mid>")
            print("   python utils/midi_inspector.py <filename.mid>")
    else:
        print("Usage: python midi.py <config_file.json>")
        print("Or use as a module: from midi import ConfigurableMIDIGenerator")
        print("\n💡 Available configs:")
        config_dir = Path('config')
        if config_dir.exists():
            for config in config_dir.glob('*.json'):
                print(f"   - {config.name}")
        print("\n🔍 Analysis tools:")
        print("   python utils/midi_analyzer.py <filename.mid>")
        print("   python utils/midi_inspector.py <filename.mid>")
