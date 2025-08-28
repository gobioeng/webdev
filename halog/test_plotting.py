"""
Test plotting functionality without GUI
Generates a sample plot to verify matplotlib integration
"""

import os
import sys
import matplotlib
# Use Agg backend for headless environment
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_plotting():
    """Test matplotlib plotting functionality"""
    try:
        print("Testing HALog Plotting Functionality")
        print("=" * 40)
        
        # Import modules
        from core.data_processor import DataProcessor
        
        print("1. Creating sample data...")
        data_processor = DataProcessor()
        data = data_processor.create_sample_data()
        
        if data is None or data.empty:
            print("   ✗ Failed to create sample data")
            return False
            
        print(f"   ✓ Sample data created: {len(data)} records")
        print(f"   ✓ Columns: {list(data.columns)}")
        
        # Create plot
        print("\n2. Creating plot...")
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Set up the plot (matching the UI implementation)
        ax.set_title("HALog - LINAC Water System Analysis", fontsize=14, fontweight='bold')
        ax.set_xlabel("Time", fontsize=12)
        ax.set_ylabel("Parameter Values", fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Plot main line using average values
        if 'avg' in data.columns:
            ax.plot(data.index, data['avg'], 'b-', linewidth=2, label='Average', alpha=0.8)
            print("   ✓ Average line plotted")
        
        # Overlay dotted lines for min and max values
        if 'min' in data.columns:
            ax.plot(data.index, data['min'], 'r:', linewidth=1.5, label='Minimum', alpha=0.7)
            print("   ✓ Minimum line plotted")
        
        if 'max' in data.columns:
            ax.plot(data.index, data['max'], 'g:', linewidth=1.5, label='Maximum', alpha=0.7)
            print("   ✓ Maximum line plotted")
        
        # Add legend with clear color coding
        ax.legend(loc='upper right', framealpha=0.9)
        print("   ✓ Legend added")
        
        # Improve layout
        fig.tight_layout()
        
        # Save plot for verification
        output_dir = os.path.join(os.path.dirname(__file__), "test_output")
        os.makedirs(output_dir, exist_ok=True)
        
        plot_file = os.path.join(output_dir, "test_plot.png")
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        print(f"   ✓ Plot saved to: {plot_file}")
        
        plt.close()
        
        # Verify file was created
        if os.path.exists(plot_file):
            file_size = os.path.getsize(plot_file)
            print(f"   ✓ Plot file size: {file_size / 1024:.1f} KB")
        else:
            print("   ✗ Plot file not created")
            return False
        
        print("\n3. Testing with real log file...")
        log_file = os.path.join(os.path.dirname(__file__), "test_data", "sample_linac.log")
        
        if os.path.exists(log_file):
            real_data = data_processor.process_file(log_file)
            
            if real_data is not None and not real_data.empty:
                print(f"   ✓ Real data processed: {len(real_data)} records")
                
                # Create plot with real data
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.set_title("HALog - Real LINAC Data Test", fontsize=14, fontweight='bold')
                ax.set_xlabel("Time", fontsize=12)
                ax.set_ylabel("Pump Pressure", fontsize=12)
                ax.grid(True, alpha=0.3)
                
                # Plot real data
                if 'avg' in real_data.columns:
                    ax.plot(real_data.index, real_data['avg'], 'b-', linewidth=2, label='Average', alpha=0.8)
                if 'min' in real_data.columns:
                    ax.plot(real_data.index, real_data['min'], 'r:', linewidth=1.5, label='Minimum', alpha=0.7)
                if 'max' in real_data.columns:
                    ax.plot(real_data.index, real_data['max'], 'g:', linewidth=1.5, label='Maximum', alpha=0.7)
                
                ax.legend(loc='upper right', framealpha=0.9)
                fig.tight_layout()
                
                real_plot_file = os.path.join(output_dir, "real_data_plot.png")
                plt.savefig(real_plot_file, dpi=150, bbox_inches='tight')
                print(f"   ✓ Real data plot saved to: {real_plot_file}")
                
                plt.close()
            else:
                print("   ✗ Failed to process real log file")
                return False
        else:
            print("   ⚠ No real log file found, skipping real data test")
        
        print("\n" + "=" * 40)
        print("✓ All plotting functionality tests passed!")
        print("\nPlot files generated successfully.")
        print("The matplotlib integration is working correctly.")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error during plotting test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_plotting():
        print("\n🎉 Plotting functionality test successful!")
        print("\nGenerated test plots can be viewed to verify visual output.")
        print("The application is ready for GUI integration with PyQt5.")
    else:
        print("\n❌ Plotting functionality test failed!")
        sys.exit(1)