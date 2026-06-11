import os
import sys
import subprocess


def main() -> None:
    app_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")

    print("=" * 60)
    print("Starting Streamlit app...")
    print("Open this URL in your browser:")
    print("http://localhost:8501")
    print("")
    print("If you are using the Android app, enter the above URL in the HTTP URL field")
    print("and use the shown Room ID in the Room ID field.")
    print("=" * 60)

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app_path,
        "--server.address",
        "0.0.0.0",
        "--server.port",
        "8501",
        "--server.headless",
        "true",
    ]

    process = subprocess.Popen(cmd, cwd=os.path.dirname(__file__))
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        process.wait()


if __name__ == "__main__":
    main()
