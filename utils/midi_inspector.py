"""
Simple MIDI Inspector - shows the raw MIDI events
"""
import mido

def inspect_midi_file(filename):
    """Print all MIDI events with timing information"""
    print(f"Inspecting MIDI file: {filename}")
    print("=" * 60)
    
    mid = mido.MidiFile(filename)
    
    print(f"File info:")
    print(f"  Type: {mid.type}")
    print(f"  Ticks per beat: {mid.ticks_per_beat}")
    print(f"  Number of tracks: {len(mid.tracks)}")
    print()
    
    for track_num, track in enumerate(mid.tracks):
        print(f"Track {track_num}:")
        print("-" * 40)
        
        current_time = 0
        for i, msg in enumerate(track):
            current_time += msg.time
            
            # Convert to musical time
            beat = current_time / mid.ticks_per_beat
            sixteenth = (current_time % (mid.ticks_per_beat // 4)) == 0
            
            if msg.type in ['note_on', 'note_off']:
                note_name = mido.format_as_string(msg)
                print(f"  {i:3d}: Time {current_time:4d} (Beat {beat:5.2f}) - {note_name}")
            elif msg.type == 'set_tempo':
                bpm = mido.tempo2bpm(msg.tempo)
                print(f"  {i:3d}: Time {current_time:4d} (Beat {beat:5.2f}) - Tempo: {bpm:.1f} BPM")
            else:
                print(f"  {i:3d}: Time {current_time:4d} (Beat {beat:5.2f}) - {msg}")
            
            if i > 50:  # Limit output for readability
                print(f"  ... (showing first 50 events only)")
                break

if __name__ == "__main__":
    inspect_midi_file("jazzy_progression_125bpm_16th_rhythm_v2.mid")
