#!/usr/bin/env python
"""
Main launcher script for the MIDI generator.
Handles the new src/ folder structure with Poetry.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / 'src'
sys.path.insert(0, str(src_dir))

def main():
    """Main entry point for the MIDI generator"""
    try:
        from midi import create_midi_from_config
        
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
                print("   poetry run python utils/midi_analyzer.py <filename.mid>")
                print("   poetry run python utils/midi_inspector.py <filename.mid>")
        else:
            print("Usage: python main.py <config_file.json>")
            print("   or: poetry run midi-generate <config_file.json>")
            print("   or: poetry run python main.py <config_file.json>")
            print("\n💡 Available configs:")
            config_dir = Path('config')
            if config_dir.exists():
                for config in config_dir.glob('*.json'):
                    print(f"   - {config.name}")
            print("\n🔍 Analysis tools:")
            print("   poetry run python utils/midi_analyzer.py <filename.mid>")
            print("   poetry run python utils/midi_inspector.py <filename.mid>")
            print("\n🧪 Testing:")
            print("   poetry run python run_tests.py")
            print("   poetry run python run_tests.py --test-only")
            print("   poetry run python run_tests.py --lint-only")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure the src/ directory contains midi.py")
        print("Try running: poetry install")
        sys.exit(1)

if __name__ == "__main__":
    main()
