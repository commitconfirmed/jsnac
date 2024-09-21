import json
import os

def infer_schema(data):
    if isinstance(data, dict):
        return {
            "type": "object",
            "properties": {k: infer_schema(v) for k, v in data.items()}
        }
    elif isinstance(data, list):
        if len(data) > 0:
            return {
                "type": "array",
                "items": infer_schema(data[0])
            }
        else:
            return {
                "type": "array",
                "items": {}
            }
    elif isinstance(data, str):
        return {"type": "string"}
    elif isinstance(data, int):
        return {"type": "integer"}
    elif isinstance(data, float):
        return {"type": "number"}
    elif isinstance(data, bool):
        return {"type": "boolean"}
    else:
        return {"type": "null"}

def json_to_schema(json_file_path, schema_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": infer_schema(data)["properties"]
    }
    
    with open(schema_file_path, 'w') as schema_file:
        json.dump(schema, schema_file, indent=4)

if __name__ == "__main__":
    json_file_path = "test.json"
    schema_file_path = "test-schema.json"
    json_to_schema(json_file_path, schema_file_path)

