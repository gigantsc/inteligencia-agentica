import os

env_paths = [
    r"C:\Users\Jean\AppData\Local\hermes\profiles\radar-conteudo\.env",
    r"C:\Users\Jean\.hermes\.env",
    r"C:\Users\Jean\AppData\Local\hermes\.env",
]

for p in env_paths:
    if os.path.exists(p):
        print("Found env file:", p)
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key_name = line.split("=", 1)[0].strip()
                    print("  Key:", key_name)
    else:
        print("Not found:", p)
