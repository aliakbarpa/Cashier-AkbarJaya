"""
AKBAR JAYA CASHIER - EXE BUILDER SCRIPT
This script will guide you through creating an executable file (.exe)
for the Akbar JAYA Cashier System using PyInstaller

Run this script first to set up everything needed.
"""

import subprocess
import sys
import os

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def run_command(command, description):
    """Run a command and show the result"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success!")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ Error:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_python():
    """Check Python version"""
    print_header("STEP 1: Checking Python Installation")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible!")
        return True
    else:
        print("❌ Python 3.8 or higher required!")
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print_header("STEP 2: Installing PyInstaller")
    return run_command(
        "pip install pyinstaller",
        "Installing PyInstaller"
    )

def check_requirements():
    """Check if all required packages are installed"""
    print_header("STEP 3: Checking Required Packages")
    packages = ['PyQt6', 'pandas']
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            print(f"   Installing {package}...")
            run_command(f"pip install {package}", f"Installing {package}")

def create_spec_file():
    """Create PyInstaller spec file for better control"""
    print_header("STEP 4: Creating PyInstaller Configuration")
    
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_prog_improved.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data', 'data'),
        ('modules', 'modules'),
        ('docs', 'docs'),
        ('receipt_improved.py', '.'),
        ('report_improved.py', '.'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtPrintSupport',
        'pandas',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AkbarJayaCashier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
"""
    
    try:
        with open('AkbarJayaCashier.spec', 'w') as f:
            f.write(spec_content)
        print("✅ Configuration file created: AkbarJayaCashier.spec")
        return True
    except Exception as e:
        print(f"❌ Error creating spec file: {e}")
        return False

def build_exe():
    """Build the executable"""
    print_header("STEP 5: Building Executable (This may take 5-10 minutes)")
    print("\n⏳ Please wait... PyInstaller is bundling everything...")
    print("   This includes Python, PyQt6, pandas, and all your code.")
    
    return run_command(
        "pyinstaller AkbarJayaCashier.spec --clean",
        "Building EXE file"
    )

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║        AKBAR JAYA CASHIER - EXE BUILDER v1.0              ║
    ║                                                            ║
    ║  This script will create a standalone .exe file           ║
    ║  that can run on any Windows computer WITHOUT             ║
    ║  requiring Python installation!                           ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Check current directory
    if not os.path.exists('main_prog_improved.py'):
        print("❌ ERROR: This script must be run from the AkbarJAYACashier folder!")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Required file: main_prog_improved.py not found")
        input("\nPress Enter to exit...")
        return
    
    # Run all steps
    steps = [
        check_python,
        install_pyinstaller,
        check_requirements,
        create_spec_file,
        build_exe
    ]
    
    for step in steps:
        if not step():
            print("\n❌ Build process failed!")
            print("   Please check the errors above and try again.")
            input("\nPress Enter to exit...")
            return
    
    # Success!
    print_header("BUILD COMPLETE! 🎉")
    print("""
    ✅ Your executable file has been created successfully!
    
    📁 Location: dist/AkbarJayaCashier.exe
    
    📝 File size: ~200-300 MB (includes Python + all libraries)
    
    ⚠️  IMPORTANT NOTES:
    
    1. The EXE file is in the 'dist' folder
    2. You need to copy these folders next to the EXE:
       • data/          (product and sales data)
       • receipts/      (for saving receipts)
       • logs/          (for activity logs)
    
    3. Folder structure should be:
       MyProgram/
       ├── AkbarJayaCashier.exe  ← The executable
       ├── data/
       ├── receipts/
       └── logs/
    
    4. To distribute:
       • Zip the entire MyProgram folder
       • Share with others
       • They can run it without installing Python!
    
    5. First run may be slow (Windows Defender scan)
       • Subsequent runs will be faster
       • You may need to allow through firewall
    
    💡 TIP: Create a shortcut to AkbarJayaCashier.exe on desktop
         for easy access!
    """)
    
    input("\n✅ Press Enter to exit...")

if __name__ == "__main__":
    main()
