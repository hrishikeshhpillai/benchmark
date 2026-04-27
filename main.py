import json
import os
import yaml
from models.example_model import CustomModel

def load_data(benchmark_name: str, catalog_path: str):

    if not os.path.exists(catalog_path):
        raise FileNotFoundError(f"Catalog file not found at {catalog_path}")

    with open(catalog_path, 'r') as f:
        catalog = yaml.safe_load(f)

    if benchmark_name not in catalog:
        available = ", ".join(catalog.keys())
        raise ValueError(f"Benchmark '{benchmark_name}' not found. Available: {available}")

    config = catalog[benchmark_name]
    json_path = config.get("json_path")
    audio_root = config.get("audio_root")
    audio_path_key = config.get("audio_path_key")

    if not os.path.exists(json_path):
         raise FileNotFoundError(f"Data file not found at {json_path}")

    with open(json_path, 'r') as f:
        dataset = json.load(f)

    print(f"Loaded config for {benchmark_name}. Resolving audio paths...")

    for item in dataset:
        relative_audio = item.get(audio_path_key) 
        
        item["full_audio_path"] = os.path.join(audio_root, relative_audio)
        
        if not os.path.exists(item["full_audio_path"]):
            print(f"Warning: Audio file missing - {item['full_audio_path']}")
            
    return dataset, config
