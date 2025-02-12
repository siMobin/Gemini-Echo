import os


def extract_path(input_string):
    if "\\>>" in input_string:
        # Extract the part after '\>>'
        path = input_string.split("\\>>", 1)[1].strip()

        # If the path starts with a quote, extract the full quoted part
        if path.startswith('"'):
            path = path.split('"', 2)[1]  # Extract the part inside quotes
        else:
            path = path.split(" ", 1)[0]  # Keep only the first word if no quotes

        # Ensure valid absolute or relative path
        if path.startswith("\\") or (len(path) > 1 and path[1] == ":"):
            return path  # Absolute path
        if "./" in path:
            return path.replace("./", "")
        else:
            return os.path.join(os.getcwd(), path)  # Relative path

    # return None
    pass


# Example usage
if __name__ == "__main__":
    input_string = input()
    print(extract_path(input_string))
