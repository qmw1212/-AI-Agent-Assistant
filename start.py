#!/usr/bin/env python
"""
Quick start script for AI Agent Assistant
"""

import os
import sys
from pathlib import Path


def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking environment...")

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False

    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("📝 Creating .env from .env.example...")

        example_file = Path(".env.example")
        if example_file.exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ .env file created")
            print("⚠️  Please edit .env and add your GOOGLE_API_KEY")
            return False
        else:
            print("❌ .env.example not found")
            return False

    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()

    nvidia_key = os.getenv("NVIDIA_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")

    if nvidia_key and nvidia_key != "your_nvidia_api_key_here":
        print("✅ NVIDIA API key configured")
    elif google_key and google_key != "your_google_api_key_here":
        print("✅ Google API key configured")
    else:
        print("❌ No API key configured in .env file")
        print("📝 Please edit .env and add one of:")
        print("   - NVIDIA_API_KEY (get at: https://build.nvidia.com/)")
        print("   - GOOGLE_API_KEY (get at: https://makersuite.google.com/app/apikey)")
        return False

    print("✅ Environment configured correctly")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    print("\n🔍 Checking dependencies...")

    required_packages = [
        "streamlit",
        "langchain",
        "google.generativeai",
        "duckduckgo_search"
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing dependencies...")
        os.system(f"{sys.executable} -m pip install -r requirements.txt")
        return True

    print("✅ All dependencies installed")
    return True


def start_app():
    """Start the Streamlit application"""
    print("\n🚀 Starting AI Agent Assistant...")
    print("📱 The app will open in your browser")
    print("🛑 Press Ctrl+C to stop\n")

    os.system("streamlit run app.py")


def main():
    """Main entry point"""
    print("=" * 50)
    print("🤖 AI Agent Assistant - Quick Start")
    print("=" * 50)

    if not check_environment():
        print("\n❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)

    if not check_dependencies():
        print("\n❌ Dependency installation failed")
        sys.exit(1)

    start_app()


if __name__ == "__main__":
    main()
