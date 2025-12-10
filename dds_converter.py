#!/usr/bin/env python3
"""
DDS Image Converter
Converts .dds files to .png and vice versa
"""

import sys
import json
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print(json.dumps({"level": "ERROR", "message": "PIL/Pillow not installed. Run: pip install Pillow"}))
    sys.exit(1)

def log(level, message):
    """Send log message to Electron"""
    print(json.dumps({"level": level, "message": message}))
    sys.stdout.flush()

def dds_to_png(input_path, output_path):
    """Convert DDS to PNG"""
    try:
        log("INFO", f"Converting DDS to PNG: {Path(input_path).name} -> {Path(output_path).name}")
        
        # Open DDS file with PIL
        with Image.open(input_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Save as PNG
            img.save(output_path, 'PNG')
        
        log("SUCCESS", f"Successfully converted to PNG")
        return True
        
    except Exception as e:
        log("ERROR", f"DDS to PNG conversion failed: {str(e)}")
        return False

def png_to_dds(input_path, output_path):
    """Convert PNG to DDS (BC3/DXT5 format)"""
    try:
        log("INFO", f"Converting PNG to DDS: {Path(input_path).name} -> {Path(output_path).name}")
        
        # Open PNG file
        with Image.open(input_path) as img:
            # Convert to RGBA
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # PIL doesn't support writing DDS directly, so we'll save as uncompressed DDS
            # For full BC3/DXT5 compression, you'd need a library like directx-dds or pyfastnoisesimd
            # This creates a basic uncompressed DDS that games can read
            
            # Save with DDS extension (PIL will write uncompressed DDS if plugin available)
            try:
                img.save(output_path, 'DDS')
                log("SUCCESS", f"Successfully converted to DDS")
            except Exception as e:
                # Fallback: Save as TGA (widely supported by games) with DDS extension
                log("WARNING", f"Direct DDS save not available, saving as uncompressed format: {str(e)}")
                
                # Create basic DDS header manually (uncompressed RGBA8)
                width, height = img.size
                data = img.tobytes()
                
                # DDS file structure (simplified, uncompressed RGBA8)
                dds_header = bytearray([
                    0x44, 0x44, 0x53, 0x20,  # Magic "DDS "
                    0x7C, 0x00, 0x00, 0x00,  # Header size (124 bytes)
                    0x07, 0x10, 0x0A, 0x00,  # Flags (CAPS | HEIGHT | WIDTH | PIXELFORMAT | LINEARSIZE)
                    height & 0xFF, (height >> 8) & 0xFF, (height >> 16) & 0xFF, (height >> 24) & 0xFF,
                    width & 0xFF, (width >> 8) & 0xFF, (width >> 16) & 0xFF, (width >> 24) & 0xFF,
                    0x00, 0x00, 0x00, 0x00,  # Pitch/LinearSize
                    0x00, 0x00, 0x00, 0x00,  # Depth
                    0x00, 0x00, 0x00, 0x00,  # MipMapCount
                ])
                
                # Reserved (11 DWORDs)
                dds_header.extend([0x00] * 44)
                
                # DDS_PIXELFORMAT structure
                dds_header.extend([
                    0x20, 0x00, 0x00, 0x00,  # Size (32 bytes)
                    0x41, 0x00, 0x00, 0x00,  # Flags (RGBA)
                    0x00, 0x00, 0x00, 0x00,  # FourCC (none for uncompressed)
                    0x20, 0x00, 0x00, 0x00,  # RGB bit count (32)
                    0x00, 0x00, 0xFF, 0x00,  # R bit mask
                    0x00, 0xFF, 0x00, 0x00,  # G bit mask
                    0xFF, 0x00, 0x00, 0x00,  # B bit mask
                    0x00, 0x00, 0x00, 0xFF,  # A bit mask
                ])
                
                # DDSCAPS2
                dds_header.extend([
                    0x08, 0x10, 0x00, 0x00,  # Caps1 (TEXTURE)
                    0x00, 0x00, 0x00, 0x00,  # Caps2
                    0x00, 0x00, 0x00, 0x00,  # Reserved
                    0x00, 0x00, 0x00, 0x00,  # Reserved
                    0x00, 0x00, 0x00, 0x00,  # Reserved
                ])
                
                # Write DDS file
                with open(output_path, 'wb') as f:
                    f.write(dds_header)
                    f.write(data)
                
                log("SUCCESS", f"Successfully converted to DDS (uncompressed RGBA8)")
        
        return True
        
    except Exception as e:
        log("ERROR", f"PNG to DDS conversion failed: {str(e)}")
        return False

def main():
    if len(sys.argv) != 4:
        print(json.dumps({"level": "ERROR", "message": "Usage: dds_converter.py <to-png|to-dds> <input> <output>"}))
        sys.exit(1)
    
    operation = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]
    
    # Check input file exists
    if not Path(input_path).exists():
        print(json.dumps({"level": "ERROR", "message": f"Input file not found: {input_path}"}))
        sys.exit(1)
    
    # Perform conversion
    if operation == "to-png":
        success = dds_to_png(input_path, output_path)
    elif operation == "to-dds":
        success = png_to_dds(input_path, output_path)
    else:
        print(json.dumps({"level": "ERROR", "message": f"Invalid operation: {operation}"}))
        sys.exit(1)
    
    # Output result
    if success:
        import os
        result = {
            "success": True,
            "output": output_path,
            "size": os.path.getsize(output_path)
        }
    else:
        result = {
            "success": False,
            "error": "Conversion failed"
        }
    
    print(f"RESULT:{json.dumps(result)}")
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
