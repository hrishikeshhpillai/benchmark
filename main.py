import json
import os
import yaml
from templates.mcq import MCQPrompt
from templates.open_ended import OpenEndedPrompt
from models.example_model import CustomModel

def load_data(benchmark_name: str, catalog_path: str = "/benchmark/catalog.yaml"):

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

def infer_mmau(output_filename: str = "mmau.json"):
    benchmark_name = "mmau"
    model = CustomModel()
    dataset, config = load_data(benchmark_name)
    question_key = config.get("question_key")
    choices_key = config.get("choices_key")
    for data in dataset:
        prompt_template = MCQPrompt(data[question_key], data[choices_key])
        prompt = prompt_template.mcq_prompt_template()
        output = model.generate(prompt, data["full_audio_path"])

        data["model_output"] = output
    
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, "w") as f:
        json.dump(dataset, f, indent=4)

    print(f"Inference complete! Saved updated dataset with 'model_output' to {output_path}")
