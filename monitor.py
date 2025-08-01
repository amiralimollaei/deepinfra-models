from dataclasses import asdict
import sys
from pathlib import Path
import os
import hashlib

# Add the project root to the path to allow a direct run
sys.path.append(str(Path(__file__).parent))
from utils import DeepinfraModelPriced, fetch_models, save_models_to_file

CACHE_DIR = Path(os.path.join(str(Path(__file__).parent), "cache"))


def create_order_independent_hash(models: set[DeepinfraModelPriced]) -> str:
    """
    Creates a hash that is independent of the order of models.
    """
    model_hashes = [str(asdict(model)) for model in models]
    model_hashes.sort()
    return hashlib.sha256(("\n".join(model_hashes)).encode("utf-8")).hexdigest()


if __name__ == "__main__":
    os.makedirs(CACHE_DIR, exist_ok=True)

    models = fetch_models()
    order_independant_hash = create_order_independent_hash(models)

    # Save models to a file
    cache_file_path = os.path.join(CACHE_DIR, f"models_{order_independant_hash}.json")
    if os.path.exists(cache_file_path):
        print(f"Cache file already exists: {cache_file_path}")
        print("Pricing is not updated, skipping saving to file.")
    else:
        print(f"Cache file does not exist: {cache_file_path}")
        print("Pricing is updated, saving models to file.")
        save_models_to_file(models, cache_file_path)
