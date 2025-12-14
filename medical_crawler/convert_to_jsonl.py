import json


def convert(input_file, output_file):
    with open(input_file) as f:
        data = json.load(f)

    with open(output_file, "w") as out:
        for item in data:
            out.write(json.dumps(item) + "\n")

convert("flexikon.json", "flexikon.jsonl")
convert("embryotox.json", "embryotox.jsonl")
convert("asa_detail.json","asa_detail.jsonl")
convert("1.json","1.jsonl")

print("JSON → JSONL conversion complete!")
