#!/usr/bin/env python3
"""
Comprehensive Test Runner for Image Interventions

This script runs multiple intervention tests and automatically generates an HTML report.
It's a convenience wrapper around test_intervention.py and generate_test_report.py.
"""

import os
import sys
import subprocess
import argparse
import time

def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"Running: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False

def discover_interventions():
    """Discover available interventions by importing the test script"""
    try:
        # Import the discovery function from test_intervention
        sys.path.insert(0, os.path.dirname(__file__))
        from test_intervention import discover_interventions
        return list(discover_interventions().keys())
    except ImportError as e:
        print(f"Failed to discover interventions: {e}")
        return ['occlusion', 'blur', 'stylization', 'replacement']  # fallback

def main():
    parser = argparse.ArgumentParser(
        description="Run multiple intervention tests and generate HTML report",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s blur occlusion          # Test blur and occlusion interventions
  %(prog)s --all                   # Test all available interventions
  %(prog)s blur --no-report        # Test blur only, don't generate report
  %(prog)s --clean --all           # Clean test directory first, then test all
        """
    )
    
    # Discover available interventions
    available_interventions = discover_interventions()
    
    parser.add_argument(
        'interventions',
        nargs='*',
        choices=available_interventions,
        help=f'Interventions to test. Available: {", ".join(available_interventions)}'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Test all available interventions'
    )
    parser.add_argument(
        '--no-report',
        action='store_true',
        help="Don't generate HTML report after testing"
    )
    parser.add_argument(
        '--no-browser',
        action='store_true',
        help="Don't automatically open report in browser"
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='Clean test output directory before running tests'
    )
    parser.add_argument(
        '--test-dir',
        default='~/Downloads/test_dir',
        help='Test output directory (default: ~/Downloads/test_dir)'
    )
    
    args = parser.parse_args()
    
    # Determine which interventions to test
    if args.all:
        interventions_to_test = available_interventions
    elif args.interventions:
        interventions_to_test = args.interventions
    else:
        parser.print_help()
        print(f"\n💡 Available interventions: {', '.join(available_interventions)}")
        print("\n🚀 Quick start: python run_tests.py --all")
        return
    
    print("🎨 Image Intervention Test Runner")
    print(f"📋 Testing interventions: {', '.join(interventions_to_test)}")
    
    # Expand test directory path
    test_dir = os.path.expanduser(args.test_dir)
    
    # Clean test directory if requested
    if args.clean:
        if os.path.exists(test_dir):
            print(f"\n🧹 Cleaning test directory: {test_dir}")
            import shutil
            shutil.rmtree(test_dir)
        os.makedirs(test_dir, exist_ok=True)
        print(f"✅ Test directory cleaned and recreated")
    else:
        # Ensure test directory exists
        os.makedirs(test_dir, exist_ok=True)
    
    # Run tests
    start_time = time.time()
    
    # Build command for test_intervention.py
    test_cmd = [sys.executable, 'test_intervention.py'] + interventions_to_test
    
    success = run_command(
        test_cmd,
        f"Testing {len(interventions_to_test)} interventions"
    )
    
    if not success:
        print("\n❌ Testing failed. Exiting.")
        sys.exit(1)
    
    # Generate report if requested
    if not args.no_report:
        report_cmd = [sys.executable, 'generate_test_report.py']
        if args.no_browser:
            report_cmd.append('--no-browser')
        if args.test_dir != '~/Downloads/test_dir':
            report_cmd.extend(['--test-dir', args.test_dir])
        
        success = run_command(
            report_cmd,
            "Generating HTML report"
        )
        
        if not success:
            print("\n⚠️  Report generation failed, but tests completed successfully.")
    
    # Summary
    elapsed_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"🎉 Test run completed in {elapsed_time:.1f} seconds")
    print(f"📁 Test outputs saved to: {test_dir}")
    if not args.no_report:
        print(f"📄 HTML report: test_results.html")
        if not args.no_browser:
            print(f"🌐 Report should open automatically in your browser")
    print('='*60)

if __name__ == "__main__":
    main()