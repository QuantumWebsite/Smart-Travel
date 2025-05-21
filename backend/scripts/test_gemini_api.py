"""
Test script for Google Generative AI (Gemini) with error handling 
and rate limit management
"""
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Gemini API with proper error handling"""
    # Get API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return
    
    try:
        import google.generativeai as genai
        from google.api_core.exceptions import GoogleAPIError, ResourceExhausted
        
        print(f"Using API key: {api_key[:5]}...{api_key[-4:]}")
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # List available models
        try:
            print("\nAvailable models:")
            models = genai.list_models()
            for model in models:
                if "generateContent" in model.supported_generation_methods:
                    print(f"- {model.name}")
        except ResourceExhausted as e:
            print(f"Rate limit exceeded when listing models: {e}")
            print("Waiting a moment before trying content generation...")
            time.sleep(2)
        except GoogleAPIError as e:
            print(f"API error when listing models: {e}")
        
        # Try content generation with proper error handling
        try:            # Use a smaller model to reduce chances of hitting rate limits
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            print("\nGenerating content...")
            response = model.generate_content("Write a very brief travel tip for packing light.")
            
            print("\nResponse:")
            print(response.text)
            
            print("\nTest completed successfully!")
        except ResourceExhausted as e:
            print(f"\nRate limit exceeded: {e}")
            print("Consider waiting a few minutes before trying again.")
            print("You could also:")
            print("- Use a different API key")
            print("- Implement request throttling")
            print("- Consider upgrading your API quota")
        except GoogleAPIError as e:
            print(f"\nGoogle API error: {e}")
        except Exception as e:
            print(f"\nUnexpected error during content generation: {e}")
            
    except ImportError as e:
        print(f"Error importing Google Generative AI library: {e}")
        print("Please install it with: pip install google-generativeai")

if __name__ == "__main__":
    test_gemini_api()