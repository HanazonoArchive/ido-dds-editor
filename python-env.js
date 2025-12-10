/**
 * Python Environment Setup
 * This script handles Python executable detection for packaged and development environments
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const { app } = require('electron');

/**
 * Get the Python executable path
 * In development: uses system Python
 * In production: uses bundled Python or system Python
 */
function getPythonPath() {
  // Check if running in packaged app
  const isPackaged = app.isPackaged;
  
  if (isPackaged) {
    // Try to use bundled Python (if you include it)
    const bundledPython = path.join(process.resourcesPath, 'python', 'python.exe');
    if (fs.existsSync(bundledPython)) {
      return bundledPython;
    }
    
    // Fallback to system Python
    // User must have Python installed
    return 'python';
  } else {
    // Development mode - use system Python
    return 'python';
  }
}

/**
 * Get the path to Python scripts
 */
function getScriptPath(scriptName) {
  const isPackaged = app.isPackaged;
  
  if (isPackaged) {
    // In production, scripts are in resources/app.asar or extraResources
    return path.join(process.resourcesPath, scriptName);
  } else {
    // In development, scripts are in the app directory
    return path.join(__dirname, scriptName);
  }
}

/**
 * Run a Python script with proper path handling
 */
function runPythonScript(scriptName, args = []) {
  const pythonPath = getPythonPath();
  const scriptPath = getScriptPath(scriptName);
  
  return spawn(pythonPath, [scriptPath, ...args]);
}

module.exports = {
  getPythonPath,
  getScriptPath,
  runPythonScript
};
