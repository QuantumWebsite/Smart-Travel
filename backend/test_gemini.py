import google.generativeai as genai
from langchain.llms import GoogleGenerativeAI

def test_direct_gemini():
    api_key = input("Enter your Google API key: ")
    
    # 1. Test the direct Google Generative AI library    print("Testing direct Google Generative AI...")
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Write a short travel packing list for a beach vacation")
    
    print(response.text)
    print("\n" + "-"*50 + "\n")
    
    # 2. Test via LangChain
    print("Testing via LangChain...")
    llm = GoogleGenerativeAI(model="gemini-2.0-flash", 
                           google_api_key=api_key,
                           temperature=0.7)
    
    response = llm.invoke("Write a short travel packing list for a beach vacation")
    
    print(response)

if __name__ == "__main__":
    test_direct_gemini()
