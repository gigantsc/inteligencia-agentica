import os, glob

dirs = [
    r"C:\Users\Jean\.hermes",
    r"C:\Users\Jean\AppData\Local\hermes",
]

for d in dirs:
    print("Checking", d)
    if os.path.exists(d):
        for root, subdirs, files in os.walk(d):
            for f in files:
                if f in [".env", "auth.json", "config.yaml"]:
                    p = os.path.join(root, f)
                    print("Found file:", p)
                    try:
                        with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                            txt = fp.read()
                            lines = [line.strip() for line in txt.splitlines() if any(k in line.lower() for k in ["gemini", "google", "imagen"])]
                            if lines:
                                print(f"  Matches in {f}: {len(lines)} lines")
                                for l in lines:
                                    print("    key line:", l.split("=")[0] if "=" in l else l[:30])
                    except Exception as e:
                        print("  Error reading:", e)
