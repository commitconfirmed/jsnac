import yaml
import json
import sys

def yaml_to_json(yaml_file, json_file):
    with open(yaml_file, 'r') as yf:
        yaml_content = yaml.safe_load(yf)
    
    with open(json_file, 'w') as jf:
        json.dump(yaml_content, jf, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test.py <input_yaml_file> <output_json_file>")
        sys.exit(1)
    
    input_yaml = sys.argv[1]
    output_json = sys.argv[2]
    
    yaml_to_json(input_yaml, output_json)