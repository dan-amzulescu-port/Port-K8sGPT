import re

from constants import UNWANTED_TEXT


def prettify_markdown(input_string: str):
    for unwanted in UNWANTED_TEXT:
        input_string = input_string.replace(unwanted, "")

    lines = input_string.split('\n')
    lines[0] = f"<span style='color:red;'>{lines[0]}</span>"
    prettified_lines = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("Error:"):
            # Handle the specific error message format
            error_match = re.search(r"Error: (.+)", stripped_line)
            if error_match:
                error_message = error_match.group(1)
                prettified_line = f"**<span style='color: red;'>Error: Kubernetes error message '{error_message}' - Solution:</span>**"
            else:
                prettified_line = f"**<span style='color: red;'>{line}</span>**"
            prettified_lines.append(prettified_line)
        elif stripped_line.startswith("Step "):
            prettified_lines.append(f"**{line}**")
        # elif stripped_line.startswith("kubectl"):
        #    prettified_lines.append(f"<span style='color: green;'>{line}</span>")
        else:
            prettified_lines.append(line)

    return '\n'.join(prettified_lines)