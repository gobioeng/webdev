#!/usr/bin/env python3
"""
Gobioeng HALog 0.0.1 beta
LINAC Machine Log File Analyzer

A professional desktop application for monitoring and analyzing 
water system parameters in Linear Accelerator (LINAC) machines 
used in radiotherapy.

Author: GoBioEng
License: MIT
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ui.main_window import MainWindow

def main():
    """Main application entry point"""
    # Create QApplication instance
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Gobioeng HALog")
    app.setApplicationVersion("0.0.1 beta")
    app.setOrganizationName("GoBioEng")
    
    # Set application icon if available
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Enable high DPI scaling for better display on modern monitors
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create and show main window
    main_window = MainWindow()
    main_window.show()
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()