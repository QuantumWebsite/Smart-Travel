import secrets
import base64
import os

def generate_secret_key(length=32):
    """
    Generate a secure random secret key suitable for JWT signing
    
    Args:
        length: Length of the secret key in bytes
        
    Returns:
        A secure random string
    """
    return secrets.token_urlsafe(length)

def generate_env_file(overwrite=False):
    """
    Generate or update .env file with a secure secret key
    
    Args:
        overwrite: Whether to overwrite an existing SECRET_KEY
    """
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    
    # Check if file exists
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            content = f.read()
        
        # Check if SECRET_KEY is already defined with a real value
        if "SECRET_KEY=" in content and "your-super-secret-key-replace-this" not in content and not overwrite:
            print("SECRET_KEY already exists in .env file. Use --overwrite to replace it.")
            return
        
        # Replace the SECRET_KEY line
        new_key = generate_secret_key(32)
        if "SECRET_KEY=" in content:
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if line.startswith("SECRET_KEY="):
                    lines[i] = f'SECRET_KEY="{new_key}"'
                    break
            
            with open(env_path, "w") as f:
                f.write("\n".join(lines))
        else:
            with open(env_path, "a") as f:
                f.write(f'\nSECRET_KEY="{new_key}"\n')
        
        print(f"Generated new SECRET_KEY in {env_path}")
    else:
        print(f"Error: .env file not found at {env_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate a secure secret key for the application")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing SECRET_KEY")
    args = parser.parse_args()
    
    generate_env_file(overwrite=args.overwrite)
