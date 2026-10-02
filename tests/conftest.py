import os
from pathlib import Path
import sys

# Same as hub/app.py: embedded apps run in Hub mode (session-memory storage, no network, demo data).
os.environ["SIGNAL_HUB"] = "1"

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
