"""
File Handler Module for HALog
Handles file operations and validation
"""

import os
import mimetypes
from pathlib import Path

class FileHandler:
    """Handles file operations for LINAC log files"""
    
    def __init__(self):
        self.supported_extensions = ['.log', '.txt', '.csv', '.dat']
        self.max_file_size = 500 * 1024 * 1024  # 500MB max file size
        
    def validate_file(self, file_path):
        """
        Validate if the file can be processed
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not os.path.exists(file_path):
            return False, "File does not exist"
            
        if not os.path.isfile(file_path):
            return False, "Path is not a file"
            
        # Check file extension
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in self.supported_extensions:
            return False, f"Unsupported file type: {file_ext}"
            
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > self.max_file_size:
            return False, f"File too large: {file_size / (1024*1024):.1f}MB (max: {self.max_file_size / (1024*1024):.1f}MB)"
            
        # Check if file is readable
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.read(100)  # Try to read first 100 characters
        except Exception as e:
            return False, f"Cannot read file: {str(e)}"
            
        return True, "File is valid"
        
    def get_file_info(self, file_path):
        """
        Get detailed information about the file
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            dict: File information
        """
        if not os.path.exists(file_path):
            return None
            
        stat = os.stat(file_path)
        
        return {
            'name': os.path.basename(file_path),
            'size': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'modified': stat.st_mtime,
            'extension': Path(file_path).suffix.lower(),
            'mime_type': mimetypes.guess_type(file_path)[0]
        }