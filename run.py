# run.py
from app import create_app
import os

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5001))
    # Bind to 0.0.0.0 for external accessibility
    app.run(host="0.0.0.0", port=port, debug=False)
