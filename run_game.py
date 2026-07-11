from pathlib import Path
import sys

project_dir = Path(__file__).resolve().parent / "Arc Hunter"
sys.path.insert(0, str(project_dir))

from main import main

if __name__ == "__main__":
    main()
