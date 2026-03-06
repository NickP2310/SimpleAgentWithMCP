"""Helper script to list available Gemini models.

Run this to see which models are available with your API key.
"""
import os
import sys
from google import genai


def main():
    """List all available Gemini models."""
    # Get API key
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ No API key found")
        print("Set GEMINI_API_KEY environment variable or pass as argument")
        print("\nUsage:")
        print("  python list_gemini_models.py")
        print("  python list_gemini_models.py YOUR_API_KEY")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    
    # Configure and list models
    print("🔍 Listing available Gemini models...\n")
    client = genai.Client(api_key=api_key)
    
    try:
        models_found = False
        for model in client.models.list():
            models_found = True
            print(f"✅ {model.name}")
            if hasattr(model, 'display_name'):
                print(f"   Display Name: {model.display_name}")
            if hasattr(model, 'description'):
                print(f"   Description: {model.description}")
            print()
        
        if not models_found:
            print("⚠️  No models found")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
