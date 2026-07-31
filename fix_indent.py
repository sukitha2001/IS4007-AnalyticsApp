with open("app.py", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if 81 <= i <= 223: # lines 82 to 224 (0-indexed 81 to 223)
        if line.startswith("    "):
            new_lines.append(line[4:])
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open("app.py", "w") as f:
    f.writelines(new_lines)
