import os
import python_minifier

root_dirs = ["agentx", "tests"]
output_dir = ".python-minifier"

for root_dir in root_dirs:
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, root_dir, os.path.relpath(root, root_dir), file)
                output_dirname = os.path.dirname(output_path)
                os.makedirs(output_dirname, exist_ok=True)
                with open(input_path) as f:
                    minified = python_minifier.minify(f.read())
                with open(output_path, "w") as f:
                    f.write(minified)