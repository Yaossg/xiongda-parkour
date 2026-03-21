import os

def parse_dialog(file_path):
    dialog = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # empty lines or comment lines are ignored
            if not line:
                continue
            if line.startswith('#'):
                continue
            if ':' not in line:
                print(f"Warning: Skipping malformed line: {line}")
                continue
            role_id, content = line.split(':', 1)
            dialog.append((int(role_id.strip()), content.strip()))
    return dialog

if __name__ == "__main__":
    dialog_file = "in/dialog.txt"
    if not os.path.exists(dialog_file):
        print(f"Error: {dialog_file} does not exist.")
    else:
        dialog = parse_dialog(dialog_file)
        for role_id, content in dialog:
            print(f"Role {role_id}: {content}")