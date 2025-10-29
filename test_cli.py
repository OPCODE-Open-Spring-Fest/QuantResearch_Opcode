#!/usr/bin/env python3
"""
Simple test script for QuantResearch CLI
This demonstrates all the CLI functionality
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd):
    """Run a command and print the result"""
    print(f"\n{'='*60}")
    print(f"Running: {cmd}")
    print('='*60)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        return False
    
    return result.returncode == 0


def main():
    """Run all CLI tests"""
    print("\n🧪 Testing QuantResearch CLI")
    print("="*60)
    
    # Define test directories
    test_data_dir = Path("test_data")
    test_output_dir = Path("test_output")
    
    # Create test directories
    test_data_dir.mkdir(exist_ok=True)
    test_output_dir.mkdir(exist_ok=True)
    
    # Test 1: Show help
    success = run_command("python -m quant_research_starter.cli --help")
    if not success:
        print("\n❌ Test 1 FAILED: Help command")
        sys.exit(1)
    
    # Test 2: Generate data
    success = run_command(
        "python -m quant_research_starter.cli generate-data "
        "-o test_data/data.csv -s 5 -d 100"
    )
    if not success:
        print("\n❌ Test 2 FAILED: Generate data")
        sys.exit(1)
    
    # Test 3: Compute factors
    success = run_command(
        "python -m quant_research_starter.cli compute-factors "
        "-d test_data/data.csv -f momentum -f value -o test_output/factors.csv"
    )
    if not success:
        print("\n❌ Test 3 FAILED: Compute factors")
        sys.exit(1)
    
    # Test 4: Run backtest
    success = run_command(
        "python -m quant_research_starter.cli backtest "
        "-d test_data/data.csv -s test_output/factors.csv "
        "-o test_output/backtest_results.json"
    )
    if not success:
        print("\n❌ Test 4 FAILED: Run backtest")
        sys.exit(1)
    
    # Verify output files exist
    print("\n📁 Checking output files...")
    files_to_check = [
        test_data_dir / "data.csv",
        test_output_dir / "factors.csv",
        test_output_dir / "backtest_results.json",
        test_output_dir / "backtest_plot.png"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if file_path.exists():
            print(f"✅ {file_path} exists ({file_path.stat().st_size} bytes)")
        else:
            print(f"❌ {file_path} missing!")
            all_exist = False
    
    if not all_exist:
        print("\n❌ Some output files are missing")
        sys.exit(1)
    
    # Summary
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print(f"\n📂 Test files created in:")
    print(f"   - {test_data_dir}/")
    print(f"   - {test_output_dir}/")
    print("\n💡 You can view the results and plots in the test_output directory.")


if __name__ == "__main__":
    main()
