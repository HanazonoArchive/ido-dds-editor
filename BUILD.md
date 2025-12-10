# Building Standalone Executables

This guide explains how to build standalone executables for IDO Editor.

## Prerequisites

### All Platforms
1. **Node.js** (v16+)
2. **Python 3.x** installed on build machine
3. Install dependencies:
   ```bash
   npm install
   npm install --save-dev electron-builder
   pip install -r requirements.txt
   ```

## Building

### Windows
```bash
npm run build:win
```

**Output:** `dist/IDO Editor Setup.exe` (installer) and `dist/IDO Editor.exe` (portable)

### macOS
```bash
npm run build:mac
```

**Output:** `dist/IDO Editor.dmg` and `dist/IDO Editor.app.zip`

### Linux
```bash
npm run build:linux
```

**Output:** `dist/IDO-Editor.AppImage` and `dist/ido-editor.deb`

## Distribution Notes

### Python Requirement
The built application **requires Python to be installed** on the user's system because:
- Python scripts are included as resources
- The app calls Python at runtime
- This keeps the package size smaller (~150MB vs 500MB+ with embedded Python)

### User Installation Instructions
Include in your releases:

**Windows:**
1. Install Python 3.x from https://www.python.org/downloads/
2. Run: `pip install Pillow`
3. Install or extract IDO Editor
4. Run the application

**macOS/Linux:**
```bash
# Install Python dependencies
pip3 install Pillow

# Run the application
./IDO Editor.app  # macOS
./IDO-Editor.AppImage  # Linux
```

## Advanced: Embedding Python (Optional)

To fully embed Python (no user installation required):

### Windows - Use Python Embeddable Package
1. Download Python embeddable zip from python.org
2. Extract to `resources/python/`
3. Update `package.json` build config:
   ```json
   "extraResources": [
     {
       "from": "resources/python",
       "to": "python"
     }
   ]
   ```
4. Update `python-env.js` to use bundled Python

**Size:** Adds ~100MB to installer

### Alternative: PyInstaller for Python Scripts
Convert Python scripts to standalone executables:

```bash
pip install pyinstaller
pyinstaller --onefile ido_tool.py
pyinstaller --onefile dds_converter.py
```

Then bundle the `.exe` files instead of `.py` scripts.

## Testing Builds

Before distribution:
1. Test on clean Windows VM (no Python installed)
2. Verify Python detection works
3. Test all features (compile, decompile, DDS convert)
4. Check for missing dependencies

## File Structure in Built App

```
IDO Editor/
├── IDO Editor.exe
├── resources/
│   ├── app.asar               # Electron code
│   ├── ido_tool.py            # Python scripts
│   ├── dds_converter.py
│   └── requirements.txt
└── ...other Electron files
```

## Troubleshooting

**"Python not found" error:**
- User needs to install Python
- Or use embedded Python approach above

**Scripts not found:**
- Check `extraResources` in package.json
- Verify `python-env.js` paths are correct

**Import errors:**
- Ensure user runs `pip install -r requirements.txt`
- Or bundle dependencies with PyInstaller
