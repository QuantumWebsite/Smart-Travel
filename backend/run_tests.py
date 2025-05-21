"""
Test runner script for Smart Travel API testing
This script provides convenient commands to run different test scenarios
"""
import argparse
import os
import sys
import subprocess

# Define color codes for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_colored(message, color=RESET):
    """Print a message with color"""
    print(f"{color}{message}{RESET}")


def run_tests(test_path=None, verbose=False, coverage=False):
    """Run pytest with specified options"""
    command = ["pytest"]
    
    if verbose:
        command.append("-v")
    
    if coverage:
        command.append("--cov=app")
    
    if test_path:
        command.append(test_path)
    
    print_colored(f"Running: {' '.join(command)}", YELLOW)
    result = subprocess.run(command)
    
    return result.returncode


def list_test_files():
    """List all available test files"""
    print_colored(f"{BOLD}Available test files:{RESET}")
    test_files = [f for f in os.listdir("tests") if f.startswith("test_") and f.endswith(".py")]
    
    for i, test_file in enumerate(sorted(test_files), 1):
        endpoint_name = test_file[5:-3]  # Remove 'test_' prefix and '.py' suffix
        print_colored(f"{i}. {test_file} - Tests for {endpoint_name} endpoints", GREEN)
    
    return test_files


def main():
    """Main function to parse arguments and run tests"""
    parser = argparse.ArgumentParser(description="Smart Travel API Test Runner")
    
    # Define command-line arguments
    parser.add_argument("-a", "--all", action="store_true", help="Run all tests")
    parser.add_argument("-f", "--file", type=str, help="Run a specific test file")
    parser.add_argument("-e", "--endpoint", type=str, help="Run tests for a specific endpoint (auth, users, search, etc.)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Run with verbose output")
    parser.add_argument("-c", "--coverage", action="store_true", help="Run with coverage report")
    parser.add_argument("-l", "--list", action="store_true", help="List available test files")
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    # List test files if requested
    if args.list:
        list_test_files()
        return 0
    
    
    # Run tests based on arguments
    if args.all:
        print_colored("Running all tests...", BOLD)
        return run_tests(verbose=args.verbose, coverage=args.coverage)
    
    if args.file:
        if not os.path.exists(args.file):
            print_colored(f"Error: File {args.file} not found", RED)
            return 1
        print_colored(f"Running tests from {args.file}...", BOLD)
        return run_tests(args.file, verbose=args.verbose, coverage=args.coverage)
    
    if args.endpoint:
        test_file = f"tests/test_{args.endpoint}.py"
        if not os.path.exists(test_file):
            print_colored(f"Error: No test file found for endpoint '{args.endpoint}'", RED)
            print_colored("Available endpoints:", YELLOW)
            test_files = list_test_files()
            return 1
        print_colored(f"Running tests for {args.endpoint} endpoints...", BOLD)
        return run_tests(test_file, verbose=args.verbose, coverage=args.coverage)


if __name__ == "__main__":
    sys.exit(main())
