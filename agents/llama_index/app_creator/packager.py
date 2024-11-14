import os
import json
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    STOP = "stop"

@dataclass
class Event:
    type: EventType
    data: Dict[str, Any]

def extract_files(code: str) -> Dict[str, str]:
    """Extract individual files from the code block"""
    files = {}
    current_file = None
    current_content = []
    
    for line in code.split('\n'):
        # Check for file markers (common formats in LLM outputs)
        if line.startswith('```') and '.' in line:
            if current_file:
                files[current_file] = '\n'.join(current_content)
                current_content = []
            current_file = line.strip('`').strip()
        elif line.startswith('```') and current_file:
            files[current_file] = '\n'.join(current_content)
            current_file = None
            current_content = []
        elif current_file:
            current_content.append(line)
            
    return files

async def packager(code: str) -> Event:
    """Package the code into individual files"""
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract files from the code block
    files = extract_files(code)
    
    # Write each file
    for filename, content in files.items():
        file_path = os.path.join(output_dir, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    # Create a manifest file
    manifest = {
        "files": list(files.keys()),
        "timestamp": str(os.path.getmtime(output_dir))
    }
    
    with open(os.path.join(output_dir, "manifest.json"), 'w') as f:
        json.dump(manifest, f, indent=2)
    
    return Event(type=EventType.STOP, data={"result": code})
