import streamlit.web.bootstrap as bootstrap
import sys

# Stop server quickly after start
def run():
    sys.argv = ["streamlit", "run", "app.py", "--server.headless", "true"]
    bootstrap.run("app.py", False, [], {})

if __name__ == "__main__":
    run()
