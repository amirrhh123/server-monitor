import json

# خواندن config از فایل JSON
with open("settings.json") as f:
    config = json.load(f)  # فایل → dict

# یا از یک رشته JSON
raw = '{"cpu": 85, "services": ["nginx"]}'
config = json.loads(raw)  # string → dict

# نوشتن JSON
data = {
    "status": "OK",
    "cpu": 72
}

with open("report.json", "w") as f:
    json.dump(data, f, indent=2)

# یا تبدیل به رشته JSON
text = json.dumps(data, indent=2)

print(type(text))