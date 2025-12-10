# IDO & DDS Compiler, Decompiler & Converter

A modern, standalone GUI application for compiling, decompiling, converting `.ido` `.dds` game asset files. Built with Electron and Python.

## Supported File Types

### Decompilation
- XML data files
- DDS/TGA/BMP/PNG textures

### Compilation
- XML files → IDO
- Binary textures (DDS, TGA, BMP, PNG) → IDO

## Installation

### Prerequisites

1. **Node.js** (v16 or higher)
2. **Python 3.x**

### Setup

1. Install dependencies:
```bash
npm install
pip install -r requirements.txt
```

2. Verify Python is accessible:
```bash
python --version
```

## Usage

### Starting the Application

```bash
npm start
```

Or for development with logging:

```bash
npm run dev
```

### Decompiling Files

1. Click the **Decompile** tab
2. Click **Browse** to select an `.ido` file
3. Choose or confirm the output location
4. Click **Start Decompilation**
5. Watch the console for real-time progress

**Output Files:**
- XML files include embedded header as comment
- Binary files have accompanying `.meta` files for recompilation

### Compiling Files

1. Click the **Compile** tab
2. Click **File** or **Folder** to select input
3. Choose the output `.ido` location
4. Click **Start Compilation**
5. Monitor the console for progress

**Requirements:**
- XML files: Header must be embedded or have `.meta` file
- Binary files: Must have corresponding `.meta` file

### Converting DDS Images

1. Click the **DDS Converter** tab
2. Choose conversion direction (DDS→PNG or PNG→DDS)
3. Click **Browse** to select input file
4. Choose output location
5. Click **Convert**

**Notes:**
- DDS to PNG: Extracts uncompressed RGBA8 image
- PNG to DDS: Creates uncompressed DDS file (compatible with most games)
- For compressed DDS formats (BC3/DXT5), use specialized tools

## Console Log Levels

- **INFO** (Blue): General information and progress
- **SUCCESS** (Green): Successful operation completion
- **WARNING** (Orange): Non-critical issues
- **ERROR** (Red): Critical failures
  
## Credits

Based on the original Rust implementation of the IDO compiler/decompiler/converter.
[ultimatuuuum](https://github.com/ultimatuuuum)
