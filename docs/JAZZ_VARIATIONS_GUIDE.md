# Professional Jazz Variations - Enhanced Configuration

## 🎼 **Musical Structure (28 bars total)**

### **I## 🎯 **Usage:**
```bash
# Generate MIDI (outputs to ./output/ folder)
python midi.py jazz_config.json

# Analyze generated MIDI (automatically checks ./output/ folder)
python utils/midi_analyzer.py jazz_variations.mid
```

### 📁 **File Organization:**
- **Configurations**: JSON files in `./config/` folder
- **Generated MIDI**: Automatically saved to `./output/` folder
- **Documentation**: Guides and docs in `./docs/` folder
- **Utilities**: Analysis tools in `./utils/` folder

This creates a complete 28-bar jazz piano piece that progresses from simple comping through melodic development to virtuosic soloing, showcasing the full range of jazz piano techniques!ars 1-4): Chord Comping**
- **Style**: Traditional jazz chord comping
- **Pattern**: Syncopated chord hits on off-beats
- **Right Hand**: Shell voicings (3rds, 7ths, extensions)
- **Tempo Feel**: Relaxed, setting the harmonic foundation

### **Verse (Bars 5-12): Melodic Line**
- **Style**: Continuous melodic phrases
- **Pattern**: Eighth note melody with chord support
- **Right Hand**: Singable melody that outlines chord changes
- **Character**: Lyrical, flowing melodic content

### **Solo (Bars 13-20): 16th Note Jazz Solo**
- **Style**: Fast bebop-style improvisation
- **Pattern**: Continuous 16th notes (jazz solo runs)
- **Right Hand**: Rapid scalar passages and arpeggios
- **Character**: Virtuosic, dense note activity, peak energy

### **Bridge (Bars 21-28): Mixed Melodic/Harmonic**
- **Style**: Combination of melody and harmony
- **Pattern**: Melodic phrases with harmonic punctuation
- **Right Hand**: Balanced melody and chord interaction
- **Character**: Musical climax with sophisticated harmony

## 🎹 **Right Hand Variations**

### **Three Different Note Sets Per Chord:**

1. **`right_hand`** - Shell voicings for comping
   ```json
   "Cm7": { "right_hand": [67, 70, 75] }  // G4, Bb4, Eb5
   ```

2. **`right_hand_melody`** - 8-note melodic phrases
   ```json
   "Cm7": { "right_hand_melody": [72, 75, 77, 75, 72, 70, 67, 70] }
   ```

3. **`right_hand_solo`** - 16-note bebop runs
   ```json
   "Cm7": { "right_hand_solo": [72, 74, 75, 77, 79, 77, 75, 74, ...] }
   ```

## 🎵 **Pattern Types**

### **Pattern Values:**
- `0` = Rest
- `1` = Chord comping
- `3` = Melodic note (uses melody array)
- `4` = Solo note (uses solo array, 16th notes)

### **Intro Pattern** (Traditional Comping):
```
[1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0]
```
- Syncopated chord hits
- Quarter note duration
- 75-65 velocity (gentle intro)

### **Verse Pattern** (Melodic):
```
[3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0]
```
- Eighth note melody
- 180ms duration (flowing)
- 85 velocity (prominent melody)

### **Solo Pattern** (16th Note Runs):
```
[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
```
- Continuous 16th notes
- 120ms duration (rapid)
- 90 velocity (peak energy)

### **Bridge Pattern** (Mixed):
```
[3, 0, 3, 3, 0, 3, 0, 3, 3, 0, 3, 3, 0, 3, 0, 3]
```
- Dense melodic activity
- 160ms duration
- 88 velocity (climactic)

## 🎯 **Musical Features**

### **Chord Progressions:**
- **ii-V-I movements** in C minor
- **Circle of fifths** harmonic motion
- **Modal interchange** (BbMaj7, EbMaj7)
- **Secondary dominants** (D7 → Gm7)

### **Melodic Content:**
- **Scalar passages** outlining chord tones
- **Chromatic approach tones** for smooth voice leading
- **Bebop-style runs** with appropriate jazz vocabulary
- **Range**: G3 to A#5 (proper intermediate piano range)

### **Dynamic Build:**
- **Intro**: 75 velocity → gentle introduction
- **Verse**: 85 velocity → clear melody
- **Solo**: 90 velocity → peak energy
- **Bridge**: 88 velocity → sustained climax

### **Jazz Techniques:**
- **Shell voicings** (3rd + 7th + extensions)
- **Rootless voicings** (bass plays roots)
- **Voice leading** between chord changes
- **Rhythmic displacement** and syncopation

## 🎵 **Usage:**
```bash
python midi.py professional_jazz_config.json
python midi_analyzer.py professional_jazz_variations.mid
```

This creates a complete 28-bar jazz piano piece that progresses from simple comping through melodic development to virtuosic soloing, showcasing the full range of jazz piano techniques!
