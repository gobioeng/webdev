# Gobioeng HALog 0.0.1 beta

**LINAC Machine Log File Analyzer**

A professional desktop application for monitoring and analyzing water system parameters in Linear Accelerator (LINAC) machines used in radiotherapy.

## Features

- **Advanced Analytics**: Comprehensive statistical analysis with min, max, and average value plotting
- **Real-time Monitoring**: Track key water parameters including pump pressure, magnetron flow, target and circulator flow
- **Efficient Data Processing**: Chunked file processing handles large log files (67K+ lines) with progress tracking
- **Professional UI**: Windows 11-style interface with proper menu positioning and responsive design
- **Graph Visualization**: Interactive plots with clear legends and color coding
- **Reset Functionality**: Easy graph reset and data reloading capabilities

## System Requirements

### Hardware Requirements
- Windows 10/11 (64-bit recommended)
- 2GB RAM minimum (4GB recommended)
- 500MB free disk space
- Screen resolution: 1280x720 or higher
- Internet connection (for updates)

### Software Dependencies
- Python 3.8 or higher (bundled with installer)
- PyQt5 for user interface
- Pandas for data processing
- Matplotlib for data visualization
- SciPy and scikit-learn for analytics

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```

3. **Test the Installation**:
   ```bash
   python test_app.py
   ```

## Supported Log Formats

- **Standard timestamp**: YYYY-MM-DD HH:MM:SS format
- **Multiple parameter name formats**
- **Statistics with count, min, max, and avg values**
- **CSV files with timestamp and value columns**
- **Detailed log files with bracketed timestamps**

## Usage

1. **Load Data**: Use File > Open to load LINAC log files
2. **View Analysis**: The graph will automatically display min, max, and average trend lines
3. **Reset Graph**: Use the Reset button or View > Reset Graph to clear current data
4. **Monitor Progress**: Large files show progress during processing

## File Format Examples

### Timestamp Stats Format
```
2025-01-01 10:00:00 pump_pressure 15 42.50 47.30 45.20
2025-01-01 11:00:00 magnetron_flow 12 10.20 14.80 12.45
```

### CSV Format
```
timestamp,parameter,value
2025-01-01 10:00:00,pump_pressure,45.20
2025-01-01 10:00:00,magnetron_flow,12.45
```

### Detailed Log Format
```
[2025-01-01 10:00:00] pump_pressure: 45.20
[2025-01-01 10:00:00] magnetron_flow: 12.45
```

## Graph Features

- **Main Line**: Blue solid line showing average values
- **Min Line**: Red dotted line showing minimum values  
- **Max Line**: Green dotted line showing maximum values
- **Interactive**: Zoom and pan capabilities
- **Professional Styling**: Clear legends with color coding

## Troubleshooting

1. **Graph not showing**: Ensure file format is supported and contains valid data
2. **Large file processing**: Use the progress bar to monitor loading status
3. **Text truncation**: Resize window or panels for better text visibility
4. **Menu positioning**: File menu is positioned at top-left following Windows 11 standards

## License

MIT License - Free for medical professionals and research use during beta testing period.

## Support

For technical support and feedback:
- GitHub: https://github.com/gobioeng/halog
- Website: https://gobioeng.com/pages/halog.html

## Version History

### 0.0.1 beta (Current)
- Initial release with core functionality
- Windows 11-style UI implementation
- Multi-format log file support
- Interactive graph visualization
- Background data processing