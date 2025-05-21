import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test the Gemini API with a simple request"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return
    
    print(f"Using API key: {api_key[:5]}...{api_key[-4:]}")
    
    try:        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Create a model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate content
        response = model.generate_content("Generate a short packing list for a beach vacation")
        
        # Print the response
        print("\nGemini API Response:")
        print(response.text)
        
        print("\nAPI test successful!")
    except Exception as e:
        print(f"\nError testing Gemini API: {e}")

if __name__ == "__main__":
    test_gemini_api()
