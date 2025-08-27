"""
Test script for HALog Application
Creates sample data and tests basic functionality
"""

import os
import sys
from datetime import datetime, timedelta
import random

def create_sample_log_file():
    """Create a sample LINAC log file for testing"""
    
    # Create test data directory
    test_dir = os.path.join(os.path.dirname(__file__), "test_data")
    os.makedirs(test_dir, exist_ok=True)
    
    # Create sample log file
    log_file = os.path.join(test_dir, "sample_linac.log")
    
    with open(log_file, 'w') as f:
        f.write("# HALog Sample LINAC Water System Log File\n")
        f.write("# Format: YYYY-MM-DD HH:MM:SS parameter count min max avg\n")
        f.write("#\n")
        
        # Generate 48 hours of hourly data
        start_time = datetime.now() - timedelta(hours=48)
        
        for i in range(48):
            timestamp = start_time + timedelta(hours=i)
            
            # Simulate different water system parameters
            parameters = [
                ("pump_pressure", 45.0, 5.0),      # Pump pressure ~45 ±5
                ("magnetron_flow", 12.5, 2.0),     # Magnetron flow ~12.5 ±2
                ("target_flow", 8.3, 1.5),         # Target flow ~8.3 ±1.5
                ("circulator_flow", 15.2, 2.5),    # Circulator flow ~15.2 ±2.5
                ("city_water_flow", 20.0, 3.0)     # City water flow ~20 ±3
            ]
            
            for param_name, base_val, variation in parameters:
                # Add some realistic variation
                noise = random.gauss(0, variation * 0.3)
                avg_val = base_val + noise
                
                # Min/Max around average
                min_val = avg_val - abs(random.gauss(variation * 0.5, variation * 0.2))
                max_val = avg_val + abs(random.gauss(variation * 0.5, variation * 0.2))
                
                count = random.randint(10, 20)  # Sample count
                
                f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} {param_name} {count} {min_val:.2f} {max_val:.2f} {avg_val:.2f}\n")
    
    print(f"Sample log file created: {log_file}")
    return log_file

def test_application():
    """Test basic application functionality"""
    try:
        # Try importing the modules
        from core.data_processor import DataProcessor
        from core.file_handler import FileHandler
        
        print("✓ Core modules imported successfully")
        
        # Test file handler
        file_handler = FileHandler()
        print("✓ FileHandler created")
        
        # Test data processor
        data_processor = DataProcessor()
        print("✓ DataProcessor created")
        
        # Create and test sample file
        sample_file = create_sample_log_file()
        
        # Validate file
        is_valid, message = file_handler.validate_file(sample_file)
        if is_valid:
            print("✓ Sample file validation passed")
        else:
            print(f"✗ Sample file validation failed: {message}")
            return False
            
        # Process file
        print("Processing sample file...")
        data = data_processor.process_file(sample_file)
        
        if data is not None and not data.empty:
            print(f"✓ File processed successfully: {len(data)} records")
            print(f"  Columns: {list(data.columns)}")
            print(f"  Date range: {data.index.min()} to {data.index.max()}")
        else:
            print("✗ File processing failed")
            return False
            
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure PyQt5 and other dependencies are installed")
        return False
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return False

if __name__ == "__main__":
    print("HALog Application Test")
    print("=" * 30)
    
    if test_application():
        print("\n✓ All tests passed! Application is ready to run.")
        print("\nTo start the application, run:")
        print("python main.py")
    else:
        print("\n✗ Some tests failed. Check the error messages above.")
        sys.exit(1)