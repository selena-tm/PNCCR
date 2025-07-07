import json
import os
import sys

def convert_recipe(data):
    # Force type to minecraft namespace
    data['type'] = 'minecraft:crafting_shaped'

    # Leave pattern as-is
    pattern = data.get("pattern", [])
    data["pattern"] = pattern

    # Reformat key values
    new_key = {}
    for symbol, entry in data.get("key", {}).items():
        # Simplify only if entry is exactly: {"item": "minecraft:..."}
        if isinstance(entry, dict) and set(entry.keys()) == {"item"}:
            new_key[symbol] = entry["item"]
        else:
            new_key[symbol] = entry  # Leave more complex cases unchanged

    data["key"] = new_key
    return data

def convert_file(path):
    with open(path, 'r') as f:
        original_data = json.load(f)

    converted_data = convert_recipe(original_data)

    with open(path, 'w') as f:
        json.dump(converted_data, f, indent=2)
    print(f"Converted: {path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_recipes.py <file_or_directory>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isdir(target):
        for filename in os.listdir(target):
            if filename.endswith(".json"):
                convert_file(os.path.join(target, filename))
    else:
        convert_file(target)

