#!/usr/bin/env python3
"""
HALog Application Launcher
Handles both GUI and command-line modes with proper error handling
"""

import sys
import os
import argparse

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    # Core dependencies
    try:
        import pandas
    except ImportError:
        missing_deps.append("pandas")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        import matplotlib
    except ImportError:
        missing_deps.append("matplotlib")
    
    # GUI dependency
    try:
        import PyQt5
    except ImportError:
        missing_deps.append("PyQt5")
    
    return missing_deps

def run_gui_mode():
    """Run the GUI application"""
    try:
        # Check if PyQt5 is available
        try:
            from PyQt5.QtWidgets import QApplication
        except ImportError:
            print("❌ PyQt5 is not installed!")
            print("To install PyQt5, run: pip install PyQt5")
            return False
        
        # Check if display is available
        if os.environ.get('DISPLAY') is None and sys.platform.startswith('linux'):
            print("❌ No display environment detected!")
            print("GUI mode requires a display environment (X11/Wayland).")
            print("Try running in command-line mode: python launcher.py --cli")
            return False
        
        # Import and run main application
        from main import main
        main()
        return True
        
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        print("Try running in command-line mode: python launcher.py --cli")
        return False

def run_cli_mode():
    """Run command-line interface mode"""
    try:
        print("HALog Command-Line Interface")
        print("=" * 40)
        
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(__file__))
        
        from core.data_processor import DataProcessor
        from core.file_handler import FileHandler
        
        # Get input file
        file_path = input("Enter path to LINAC log file: ").strip()
        
        if not file_path:
            print("No file specified.")
            return False
        
        # Validate file
        file_handler = FileHandler()
        is_valid, message = file_handler.validate_file(file_path)
        
        if not is_valid:
            print(f"❌ File validation failed: {message}")
            return False
        
        print(f"✓ File validated: {os.path.basename(file_path)}")
        
        # Process file
        print("Processing file...")
        data_processor = DataProcessor()
        
        def progress_callback(progress):
            print(f"Progress: {progress}%")
        
        data = data_processor.process_file(file_path, progress_callback)
        
        if data is not None and not data.empty:
            print(f"\n✓ File processed successfully!")
            print(f"Records: {len(data)}")
            print(f"Columns: {list(data.columns)}")
            print(f"Date range: {data.index.min()} to {data.index.max()}")
            
            if 'avg' in data.columns:
                print(f"Average value range: {data['avg'].min():.2f} - {data['avg'].max():.2f}")
            
            # Generate plot
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            
            print("\nGenerating plot...")
            fig, ax = plt.subplots(figsize=(12, 8))
            
            ax.set_title("HALog - LINAC Water System Analysis", fontsize=14, fontweight='bold')
            ax.set_xlabel("Time", fontsize=12)
            ax.set_ylabel("Parameter Values", fontsize=12)
            ax.grid(True, alpha=0.3)
            
            if 'avg' in data.columns:
                ax.plot(data.index, data['avg'], 'b-', linewidth=2, label='Average', alpha=0.8)
            if 'min' in data.columns:
                ax.plot(data.index, data['min'], 'r:', linewidth=1.5, label='Minimum', alpha=0.7)
            if 'max' in data.columns:
                ax.plot(data.index, data['max'], 'g:', linewidth=1.5, label='Maximum', alpha=0.7)
            
            ax.legend(loc='upper right', framealpha=0.9)
            fig.tight_layout()
            
            # Save plot
            output_file = os.path.splitext(file_path)[0] + "_analysis.png"
            plt.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close()
            
            print(f"✓ Analysis plot saved to: {output_file}")
            
        else:
            print("❌ Failed to process file")
            return False
        
        return True
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return False
    except Exception as e:
        print(f"❌ Error in CLI mode: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_test_mode():
    """Run application tests"""
    try:
        print("Running HALog Tests")
        print("=" * 30)
        
        # Run core tests
        from test_core import test_core_functionality
        if not test_core_functionality():
            return False
        
        print("\n" + "-" * 30)
        
        # Run plotting tests
        from test_plotting import test_plotting
        if not test_plotting():
            return False
        
        print("\n🎉 All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="HALog - LINAC Machine Log File Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launcher.py              # Run GUI mode (default)
  python launcher.py --gui        # Run GUI mode explicitly
  python launcher.py --cli        # Run command-line mode
  python launcher.py --test       # Run tests
  python launcher.py --check      # Check dependencies
        """
    )
    
    parser.add_argument('--gui', action='store_true', 
                       help='Run in GUI mode (default)')
    parser.add_argument('--cli', action='store_true',
                       help='Run in command-line mode')
    parser.add_argument('--test', action='store_true',
                       help='Run application tests')
    parser.add_argument('--check', action='store_true',
                       help='Check dependencies')
    
    args = parser.parse_args()
    
    # Display header
    print("Gobioeng HALog 0.0.1 beta")
    print("LINAC Machine Log File Analyzer")
    print("-" * 40)
    
    # Check dependencies if requested
    if args.check or not any([args.gui, args.cli, args.test]):
        print("Checking dependencies...")
        missing_deps = check_dependencies()
        
        if missing_deps:
            print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
            print(f"\nTo install missing dependencies, run:")
            print(f"pip install {' '.join(missing_deps)}")
            return False
        else:
            print("✓ All dependencies are available")
            
        if args.check:
            return True
    
    # Run in requested mode
    success = False
    
    if args.test:
        success = run_test_mode()
    elif args.cli:
        success = run_cli_mode()
    else:  # Default to GUI mode
        success = run_gui_mode()
    
    if not success:
        print("\n❌ Operation failed. See error messages above.")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)