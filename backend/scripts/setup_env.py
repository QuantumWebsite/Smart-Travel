import os
import sys
import shutil
from generate_key import generate_secret_key

# Add parent directory to path so we can import core modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_env_example():
    """
    Create a .env.example file with placeholders but no actual secrets
    """
    env_example_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env.example")
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    
    # If .env exists, create .env.example based on it
    if os.path.exists(env_path):
        with open(env_path, "r") as env_file:
            content = env_file.read()
            
        # Replace actual secrets with placeholders
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.split("=", 1)
                # Check if value appears to be a secret (contains actual content)
                if value.strip() and "your_" not in value and "your-" not in value:
                    lines[i] = f"{key}=your_{key.lower()}_here"
        
        with open(env_example_path, "w") as example_file:
            example_file.write("\n".join(lines))
        
        print(f"Created .env.example file at {env_example_path}")
    else:
        print(f"Error: .env file not found at {env_path}")

def setup_env():
    """
    Guide the user through setting up the .env file
    """
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    env_example_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env.example")
    
    # If .env doesn't exist but .env.example does, copy it
    if not os.path.exists(env_path) and os.path.exists(env_example_path):
        shutil.copy(env_example_path, env_path)
        print(f"Created .env file from .env.example at {env_path}")
    
    # Generate a secure SECRET_KEY
    with open(env_path, "r") as f:
        content = f.read()
    
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("SECRET_KEY="):
            if "your-super-secret-key-replace-this" in line or "your_secret_key_here" in line:
                lines[i] = f'SECRET_KEY="{generate_secret_key(32)}"'
                print("Generated new SECRET_KEY")
    
    with open(env_path, "w") as f:
        f.write("\n".join(lines))
    
    print("\nPlease review your .env file and fill in any missing values.")
    print("The following values need to be set for the application to work properly:")
    print("- POSTGRES_PASSWORD (secure database password)")
    print("- BRIGHT_DATA_API_KEY (if using Bright Data scraping)")
    print("- BRIGHT_DATA_ZONE_USERNAME (if using Bright Data scraping)")
    print("- BRIGHT_DATA_ZONE_PASSWORD (if using Bright Data scraping)")
    print("\nOptional but recommended:")
    print("- Enable any needed API keys by uncommenting their lines")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Set up environment variables for Smart Travel API")
    parser.add_argument("--create-example", action="store_true", help="Create .env.example file")
    args = parser.parse_args()
    
    if args.create_example:
        create_env_example()
    else:
        setup_env()
