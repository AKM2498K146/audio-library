#!/usr/bin/env python3
"""
Generate audio library index from directory structure.
"""

import json
import os
from pathlib import Path
from datetime import datetime

SUPPORTED_FORMATS = {
    'sf2', 'mp3', 'wav', 'flac', 'm4a', 'aac', 
    'amr', 'ogg', 'opus', 'wma', 'mid', 'midi'
}

AUDIO_ROOT = Path(__file__).parent.parent
CATALOG_FILE = AUDIO_ROOT / 'metadata' / 'catalog.json'


def scan_audio_files():
    """Scan for audio files in the library."""
    audio_sources = []
    
    for root, dirs, files in os.walk(AUDIO_ROOT):
        # Skip metadata and docs directories
        dirs[:] = [d for d in dirs if d not in {'metadata', 'docs', '.git', 'scripts'}]
        
        for file in files:
            ext = file.split('.')[-1].lower()
            if ext in SUPPORTED_FORMATS:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(AUDIO_ROOT).as_posix()
                
                audio_sources.append({
                    'id': file_path.stem,
                    'name': file_path.stem.replace('_', ' '),
                    'path': relative_path,
                    'format': ext,
                    'size_bytes': file_path.stat().st_size,
                    'date_added': datetime.now().isoformat()
                })
    
    return sorted(audio_sources, key=lambda x: x['path'])


def update_catalog(audio_sources):
    """Update catalog.json with discovered files."""
    with open(CATALOG_FILE, 'r') as f:
        catalog = json.load(f)
    
    catalog['audio_sources'] = audio_sources
    catalog['total_items'] = len(audio_sources)
    catalog['last_updated'] = datetime.now().isoformat()
    
    with open(CATALOG_FILE, 'w') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    
    return catalog


def main():
    """Main function."""
    print("📀 Scanning audio library...")
    audio_sources = scan_audio_files()
    
    if audio_sources:
        print(f"✅ Found {len(audio_sources)} audio files")
        catalog = update_catalog(audio_sources)
        print(f"✅ Updated {CATALOG_FILE}")
        print(f"\n📊 Summary:")
        print(f"   Total files: {len(audio_sources)}")
        print(f"   Last updated: {catalog['last_updated']}")
    else:
        print("⚠️  No audio files found")


if __name__ == '__main__':
    main()
