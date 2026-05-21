# scripts/txt_to_jsonl.py
import os, json, glob

data_dir = "D:\Emotions"            # your folder with txt files
out_file = os.path.join(data_dir, "jarvis_emotion.jsonl")

lines_out = []
for fname in glob.glob(os.path.join(data_dir, "*.txt")):
    with open(fname, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: 
                continue
            # assume format: text;emotion
            if ";" in line:
                text, label = line.rsplit(";", 1)
            elif "\t" in line:
                text, label = line.rsplit("\t", 1)
            else:
                # skip or put into 'unknown'
                continue
            prompt = f"Classify the emotion of the following text:\n\n{text}\n\nEmotion:"
            completion = " " + label.strip()  # leading space is typical in jsonl
            obj = {"prompt": prompt, "completion": completion}
            lines_out.append(obj)

with open(out_file, "w", encoding="utf-8") as out:
    for obj in lines_out:
        out.write(json.dumps(obj, ensure_ascii=False) + "\n")

print(f"Wrote {len(lines_out)} examples to {out_file}")
