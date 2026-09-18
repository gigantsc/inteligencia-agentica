import os

found = []
for k, v in os.environ.items():
    if "KEY" in k.upper() or "TOKEN" in k.upper() or "GEMINI" in k.upper() or "GOOGLE" in k.upper():
        found.append((k, len(v)))
print("Env keys:", found)
