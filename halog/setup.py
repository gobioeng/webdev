"""
Setup script for HALog Application
Installs dependencies and prepares the application for use
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages"""
    requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements_file):
        print("❌ requirements.txt not found!")
        return False
        
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_desktop_shortcut():
    """Create a desktop shortcut for Windows"""
    try:
        if sys.platform == "win32":
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "HALog.lnk")
            target = os.path.join(os.path.dirname(__file__), "main.py")
            wdir = os.path.dirname(__file__)
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = f'"{target}"'
            shortcut.WorkingDirectory = wdir
            shortcut.Description = "Gobioeng HALog - LINAC Log Analyzer"
            shortcut.save()
            
            print("🔗 Desktop shortcut created!")
            return True
    except ImportError:
        print("ℹ️  Desktop shortcut creation requires winshell package (optional)")
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")
    
    return False

def main():
    """Main setup function"""
    print("🚀 HALog Setup")
    print("=" * 50)
    print("Setting up Gobioeng HALog 0.0.1 beta")
    print("LINAC Machine Log File Analyzer")
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Test installation
    print("\n🧪 Testing installation...")
    try:
        from test_app import test_application
        if test_application():
            print("✅ Installation test passed!")
        else:
            print("❌ Installation test failed!")
            return False
    except Exception as e:
        print(f"❌ Installation test error: {e}")
        return False
    
    # Create desktop shortcut
    print("\n🔗 Creating shortcuts...")
    create_desktop_shortcut()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print()
    print("To run HALog:")
    print(f"  python {os.path.join(os.path.dirname(__file__), 'main.py')}")
    print()
    print("Or double-click the desktop shortcut if created.")
    print()
    print("For help and documentation, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)