"""
Convenience script to run both backend API and frontend UI
"""
import subprocess
import sys
import os
import time
import signal

def check_port_available(port):
    """Check if a port is available"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except:
            return False

def main():
    """Run both backend and frontend"""
    print("🚀 Starting PR Review Agent (Backend + Frontend)")
    print("=" * 60)
    
    # Check if ports are available
    if not check_port_available(8000):
        print("⚠️  Port 8000 is already in use (Backend API)")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    if not check_port_available(8501):
        print("⚠️  Port 8501 is already in use (Frontend UI)")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print()
    print("📍 Backend API will run on: http://localhost:8000")
    print("📍 Frontend UI will run on: http://localhost:8501")
    print()
    print("Press Ctrl+C to stop both services")
    print("=" * 60)
    print()
    
    # Start backend
    print("🔧 Starting backend API...")
    backend_process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Start frontend
    print("🎨 Starting frontend UI...")
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "app.py")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", frontend_path,
         "--server.port=8501",
         "--server.address=localhost"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    print()
    print("✅ Both services started!")
    print()
    print("📖 Open your browser to: http://localhost:8501")
    print()
    
    def signal_handler(sig, frame):
        print("\n\n🛑 Stopping services...")
        backend_process.terminate()
        frontend_process.terminate()
        print("👋 Services stopped")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Monitor both processes
        while True:
            # Check if either process died
            if backend_process.poll() is not None:
                print("❌ Backend process died!")
                frontend_process.terminate()
                sys.exit(1)
            
            if frontend_process.poll() is not None:
                print("❌ Frontend process died!")
                backend_process.terminate()
                sys.exit(1)
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping services...")
        backend_process.terminate()
        frontend_process.terminate()
        print("👋 Services stopped")

if __name__ == "__main__":
    main()
