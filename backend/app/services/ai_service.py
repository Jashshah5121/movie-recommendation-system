import sys
from pathlib import Path

# -------------------------------------------------
# Add ML folder to Python path
# -------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[3]
ML_DIR = ROOT_DIR / "ml"

if str(ML_DIR) not in sys.path:
    sys.path.append(str(ML_DIR))

# -------------------------------------------------
# Import AI Pipeline
# -------------------------------------------------

from pipeline.ai_pipeline import AIPipeline


class AIService:

    @staticmethod
    def search(query: str):

        return AIPipeline.search(
            query=query,
            top_k=12
        )