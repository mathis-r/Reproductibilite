import json, subprocess, sys

out = subprocess.run([sys.executable, "cli.py", "--repetitions", "100"],
                     capture_output=True, text=True).stdout
answer = json.loads(out)
print(answer)
for rep in [100,1000,10000]:
    for min,max in [(0.0,1.0),(0.0,50.0)]:
        out = subprocess.run([sys.executable, "cli.py", "--repetitions", str(rep), "--minrand", str(min), "--maxrand", str(max)], capture_output=True, text=True).stdout
        answer = json.loads(out)
        print(answer)