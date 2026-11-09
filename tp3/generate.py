import subprocess
import sys
from pathlib import Path
from jinja2 import Template
import numpy as np

template = Template(Path("assoc.py.jinja").read_text())
properties = {"assoc_add": ("(x + y) + z", "x + (y + z)"),
              "assoc_mul": ("(x * y) * z", "x * (y * z)")}
types = ["float","np.float32","np.float16","np.float128"] # double, simple, demi, et quadruple précision
Path("generated").mkdir(exist_ok=True)
for name, (lhs, rhs) in properties.items():
    for type in types:
        path = Path(f"generated/{name}_{type}.py")
        path.write_text(template.render(lhs=lhs, rhs=rhs, repetitions=10000,type=type))
        result = subprocess.run([sys.executable, path], capture_output=True, text=True)
        print(name, type, result.stdout.strip(), result.stderr.strip())