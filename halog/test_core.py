"""
Test core functionality without GUI
Tests data processing and file handling modules
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

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
        
        # Generate 24 hours of hourly data
        start_time = datetime.now() - timedelta(hours=24)
        
        for i in range(24):
            timestamp = start_time + timedelta(hours=i)
            
            # Simulate pump pressure data
            base_val = 45.0
            variation = 5.0
            noise = random.gauss(0, variation * 0.3)
            avg_val = base_val + noise
            
            min_val = avg_val - abs(random.gauss(variation * 0.5, variation * 0.2))
            max_val = avg_val + abs(random.gauss(variation * 0.5, variation * 0.2))
            
            count = random.randint(10, 20)
            
            f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} pump_pressure {count} {min_val:.2f} {max_val:.2f} {avg_val:.2f}\n")
    
    return log_file

def test_core_functionality():
    """Test core functionality without GUI"""
    try:
        print("Testing HALog Core Functionality")
        print("=" * 40)
        
        # Test imports
        print("1. Testing imports...")
        from core.data_processor import DataProcessor
        from core.file_handler import FileHandler
        print("   ✓ Core modules imported successfully")
        
        # Test file handler
        print("\n2. Testing FileHandler...")
        file_handler = FileHandler()
        print("   ✓ FileHandler created")
        
        # Test data processor
        print("\n3. Testing DataProcessor...")
        data_processor = DataProcessor()
        print("   ✓ DataProcessor created")
        
        # Create and test sample file
        print("\n4. Creating sample log file...")
        sample_file = create_sample_log_file()
        print(f"   ✓ Sample file created: {sample_file}")
        
        # Validate file
        print("\n5. Validating file...")
        is_valid, message = file_handler.validate_file(sample_file)
        if is_valid:
            print("   ✓ Sample file validation passed")
        else:
            print(f"   ✗ Sample file validation failed: {message}")
            return False
            
        # Get file info
        print("\n6. Getting file information...")
        file_info = file_handler.get_file_info(sample_file)
        if file_info:
            print(f"   ✓ File size: {file_info['size_mb']:.2f} MB")
            print(f"   ✓ File extension: {file_info['extension']}")
        
        # Process file
        print("\n7. Processing sample file...")
        data = data_processor.process_file(sample_file)
        
        if data is not None and not data.empty:
            print(f"   ✓ File processed successfully: {len(data)} records")
            print(f"   ✓ Columns: {list(data.columns)}")
            print(f"   ✓ Date range: {data.index.min()} to {data.index.max()}")
            
            # Test data content
            if 'min' in data.columns and 'max' in data.columns and 'avg' in data.columns:
                print(f"   ✓ Average value range: {data['avg'].min():.2f} - {data['avg'].max():.2f}")
                print(f"   ✓ Min value range: {data['min'].min():.2f} - {data['min'].max():.2f}")
                print(f"   ✓ Max value range: {data['max'].min():.2f} - {data['max'].max():.2f}")
        else:
            print("   ✗ File processing failed")
            return False
        
        # Test sample data generation
        print("\n8. Testing sample data generation...")
        sample_data = data_processor.create_sample_data()
        if sample_data is not None and not sample_data.empty:
            print(f"   ✓ Sample data generated: {len(sample_data)} records")
        
        print("\n" + "=" * 40)
        print("✓ All core functionality tests passed!")
        print("\nThe application core is working correctly.")
        print("GUI components require PyQt5 and a display environment.")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_core_functionality():
        print("\n🎉 Core functionality test successful!")
        print("\nTo run the full GUI application:")
        print("1. Install PyQt5: pip install PyQt5")
        print("2. Run: python main.py")
    else:
        print("\n❌ Core functionality test failed!")
        sys.exit(1)