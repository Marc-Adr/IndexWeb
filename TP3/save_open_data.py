import json

def open_jsonl(file_path): # To open a jsonl file
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))  #convert every line into json
    return data

def open_json(file_path): # To open a json file
    with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    return data

# To save any index or result of the research 
def save_data(index, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=4)