"""
Main Window for HALog Application
Implements the primary UI with Windows 11 styling and proper menu layout
"""

import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QMenuBar, QAction, QFileDialog, QTextEdit, QSplitter,
                           QGroupBox, QPushButton, QLabel, QProgressBar, QStatusBar,
                           QMessageBox, QFrame)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from core.data_processor import DataProcessor
from core.file_handler import FileHandler

class DataProcessingThread(QThread):
    """Background thread for processing large data files"""
    progress_updated = pyqtSignal(int)
    data_ready = pyqtSignal(object)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        try:
            processor = DataProcessor()
            data = processor.process_file(self.file_path, progress_callback=self.progress_updated.emit)
            self.data_ready.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))

class GraphWidget(QWidget):
    """Custom widget for matplotlib graphs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(12, 8), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        
        # Add reset button
        self.reset_button = QPushButton("Reset Graph")
        self.reset_button.clicked.connect(self.reset_graph)
        self.reset_button.setMaximumWidth(120)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Initialize empty plot
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("HALog - LINAC Water System Analysis")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Parameter Values")
        self.canvas.draw()
        
    def plot_data(self, data):
        """Plot data with min, max, and average lines"""
        if data is None or data.empty:
            return
            
        self.ax.clear()
        
        # Set up the plot
        self.ax.set_title("HALog - LINAC Water System Analysis", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Time", fontsize=12)
        self.ax.set_ylabel("Parameter Values", fontsize=12)
        self.ax.grid(True, alpha=0.3)
        
        # Plot main line using average values
        if 'avg' in data.columns:
            self.ax.plot(data.index, data['avg'], 'b-', linewidth=2, label='Average', alpha=0.8)
        
        # Overlay dotted lines for min and max values
        if 'min' in data.columns:
            self.ax.plot(data.index, data['min'], 'r:', linewidth=1.5, label='Minimum', alpha=0.7)
        
        if 'max' in data.columns:
            self.ax.plot(data.index, data['max'], 'g:', linewidth=1.5, label='Maximum', alpha=0.7)
        
        # Add legend with clear color coding
        self.ax.legend(loc='upper right', framealpha=0.9)
        
        # Improve layout
        self.figure.tight_layout()
        self.canvas.draw()
        
    def reset_graph(self):
        """Clear the current graph and allow reloading fresh data"""
        self.ax.clear()
        self.ax.set_title("HALog - LINAC Water System Analysis")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Parameter Values")
        self.ax.text(0.5, 0.5, "No data loaded\nUse File > Open to load LINAC log data", 
                    ha='center', va='center', transform=self.ax.transAxes, 
                    fontsize=12, alpha=0.6)
        self.canvas.draw()

class MainWindow(QMainWindow):
    """Main application window with Windows 11 styling"""
    
    def __init__(self):
        super().__init__()
        self.data = None
        self.processing_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        # Set window properties with correct title
        self.setWindowTitle("Gobioeng HALog 0.0.1 beta")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        
        # Apply Windows 11 style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #cccccc;
                padding: 4px;
                font-size: 11px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #e3f2fd;
            }
            QMenuBar::item:pressed {
                background-color: #bbdefb;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QGroupBox {
                font-weight: 600;
                border: 2px solid #cccccc;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10px;
            }
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: #f0f0f0;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 3px;
            }
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #cccccc;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Create menu bar (positioned at top-left following Windows 11 style)
        self.create_menu_bar()
        
        # Create main content area with splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel for controls and info
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel for graph
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions (30% left, 70% right)
        splitter.setSizes([360, 840])
        main_layout.addWidget(splitter)
        
        # Create status bar
        self.create_status_bar()
        
        # Create progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
    def create_menu_bar(self):
        """Create Windows 11 style menu bar positioned at top-left"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Open action
        open_action = QAction('Open Log File...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open LINAC log file for analysis')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        # Reset graph action
        reset_action = QAction('Reset Graph', self)
        reset_action.setShortcut('Ctrl+R')
        reset_action.setStatusTip('Reset graph and clear data')
        reset_action.triggered.connect(self.reset_graph)
        view_menu.addAction(reset_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        # About action
        about_action = QAction('About HALog', self)
        about_action.setStatusTip('About this application')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_left_panel(self):
        """Create left panel with controls and information"""
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        # File information group
        file_group = QGroupBox("File Information")
        file_layout = QVBoxLayout()
        
        self.file_info_label = QLabel("No file loaded")
        self.file_info_label.setWordWrap(True)
        file_layout.addWidget(self.file_info_label)
        
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)
        
        # Data summary group
        summary_group = QGroupBox("Data Summary")
        summary_layout = QVBoxLayout()
        
        self.summary_text = QTextEdit()
        self.summary_text.setMaximumHeight(200)
        self.summary_text.setPlainText("Load a log file to see data summary...")
        summary_layout.addWidget(self.summary_text)
        
        summary_group.setLayout(summary_layout)
        left_layout.addWidget(summary_group)
        
        # Controls group
        controls_group = QGroupBox("Controls")
        controls_layout = QVBoxLayout()
        
        self.load_button = QPushButton("Load Log File")
        self.load_button.clicked.connect(self.open_file)
        controls_layout.addWidget(self.load_button)
        
        self.reset_button = QPushButton("Reset Graph")
        self.reset_button.clicked.connect(self.reset_graph)
        controls_layout.addWidget(self.reset_button)
        
        controls_group.setLayout(controls_layout)
        left_layout.addWidget(controls_group)
        
        # Add stretch to push everything to top
        left_layout.addStretch()
        
        left_widget.setLayout(left_layout)
        left_widget.setMaximumWidth(400)
        return left_widget
        
    def create_right_panel(self):
        """Create right panel with graph"""
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        # Graph group
        graph_group = QGroupBox("LINAC Water System Analysis")
        graph_layout = QVBoxLayout()
        
        # Create graph widget
        self.graph_widget = GraphWidget()
        graph_layout.addWidget(self.graph_widget)
        
        graph_group.setLayout(graph_layout)
        right_layout.addWidget(graph_group)
        
        right_widget.setLayout(right_layout)
        return right_widget
        
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Load a LINAC log file to begin analysis")
        
    def open_file(self):
        """Open file dialog and load LINAC log file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open LINAC Log File",
            "",
            "Log Files (*.log *.txt *.csv);;All Files (*)"
        )
        
        if file_path:
            self.load_file(file_path)
            
    def load_file(self, file_path):
        """Load and process the selected file"""
        try:
            # Update UI
            self.status_bar.showMessage(f"Loading file: {os.path.basename(file_path)}")
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Update file info
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            self.file_info_label.setText(
                f"File: {os.path.basename(file_path)}\n"
                f"Size: {file_size_mb:.1f} MB\n"
                f"Path: {file_path}"
            )
            
            # Start background processing
            self.processing_thread = DataProcessingThread(file_path)
            self.processing_thread.progress_updated.connect(self.update_progress)
            self.processing_thread.data_ready.connect(self.data_loaded)
            self.processing_thread.error_occurred.connect(self.handle_error)
            self.processing_thread.start()
            
        except Exception as e:
            self.handle_error(f"Error loading file: {str(e)}")
            
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
        
    def data_loaded(self, data):
        """Handle data loading completion"""
        self.data = data
        self.progress_bar.setVisible(False)
        
        if data is not None and not data.empty:
            # Update summary
            summary = f"Records: {len(data)}\n"
            if 'avg' in data.columns:
                summary += f"Average range: {data['avg'].min():.2f} - {data['avg'].max():.2f}\n"
            if 'min' in data.columns:
                summary += f"Minimum value: {data['min'].min():.2f}\n"
            if 'max' in data.columns:
                summary += f"Maximum value: {data['max'].max():.2f}\n"
            
            self.summary_text.setPlainText(summary)
            
            # Plot the data
            self.graph_widget.plot_data(data)
            self.status_bar.showMessage("Data loaded successfully - Graph updated")
        else:
            self.handle_error("No valid data found in file")
            
    def handle_error(self, error_message):
        """Handle errors during file processing"""
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(f"Error: {error_message}")
        
        QMessageBox.critical(self, "Error", f"An error occurred:\n\n{error_message}")
        
    def reset_graph(self):
        """Reset graph and clear data"""
        self.data = None
        self.graph_widget.reset_graph()
        self.summary_text.setPlainText("Load a log file to see data summary...")
        self.file_info_label.setText("No file loaded")
        self.status_bar.showMessage("Graph reset - Load a LINAC log file to begin analysis")
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About HALog",
            "<h3>Gobioeng HALog 0.0.1 beta</h3>"
            "<p>LINAC Machine Log File Analyzer</p>"
            "<p>A professional desktop application for monitoring and analyzing "
            "water system parameters in Linear Accelerator (LINAC) machines "
            "used in radiotherapy.</p>"
            "<p><b>Author:</b> GoBioEng<br>"
            "<b>Version:</b> 0.0.1 beta<br>"
            "<b>License:</b> MIT</p>"
        )