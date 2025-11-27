"""
Convenience script to run the Streamlit frontend
"""
import subprocess
import sys
import os

def main():
    """Run the Streamlit frontend"""
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "app.py")
    
    if not os.path.exists(frontend_path):
        print("❌ Frontend app not found at:", frontend_path)
        sys.exit(1)
    
    print("🚀 Starting PR Review Agent Frontend...")
    print("📍 Frontend will be available at: http://localhost:8501")
    print("📍 Make sure the backend API is running at: http://localhost:8000")
    print()
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            frontend_path,
            "--server.port=8501",
            "--server.address=localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Frontend stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
