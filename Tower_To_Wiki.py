import tkinter as tk
from tkinter import filedialog
from slpp import slpp as lua
import os
import re

selected_File = None

def select_File():
    global selected_File

    root = tk.Tk()
    root.withdraw()
    root.update()

    file_path = filedialog.askopenfilename(
        title = "Select tower's lua file to export.",
        filetypes = [("Lua files", "*.lua"), ("All files", "*.*")]
    )
    root.destroy()

    if file_path:
        selected_File = file_path
        print(f"Selected File: {selected_File}")
    else:
        print("No file selected.")
    menu()
    return file_path

def load_lua_Table(filePath):

    with open(filePath, "r", encoding="utf8") as f:
        content = f.read()

    content = re.sub(r"^return", "", content.strip())
    return lua.decode(content)

def generate_upgrade_table(upgrades):
    # Convert list → dict with numeric keys if needed
    if isinstance(upgrades, list):
        upgrades = {i: v for i, v in enumerate(upgrades)}

    headers = set()
    for lvl in upgrades.values():
        headers.update(lvl.keys())
    headers = sorted(headers)

    table = '{| class="wikitable"\n'
    table += "! Level " + "".join([f"!! {h}" for h in headers]) + "\n"

    for lvl_num, stats in sorted(upgrades.items()):
        table += "|-\n"
        table += f"| {lvl_num} "
        for h in headers:
            val = stats.get(h, "-")
            if isinstance(val, bool):
                val = str(val)
            table += f"|| {val}"
        table += "\n"

    table += "|}\n"
    return table

# ---------------------------
# Generate full wiki text for one tower
# ---------------------------
def generate_tower_wiki(name, tower_data):
    # Header info
    header = f"== {name} ==\n\n"
    header += f"* Type: {tower_data.get('Type', '-')}\n"
    header += f"* Description: {tower_data.get('Description', '-')}\n"
    header += f"* ShopPrice: {tower_data.get('ShopPrice', '-')}\n\n"

    # Upgrades
    upgrades = tower_data.get("Upgrades", {})
    upgrade_table = generate_upgrade_table(upgrades)

    return header + "=== Upgrades ===\n" + upgrade_table

# ---------------------------
# Wiki preview UI
# ---------------------------
def wiki_text_preview(wiki_text):
    root = tk.Tk()
    root.title("Wiki Preview")
    text = tk.Text(root, wrap="word", width=80, height=30)
    text.insert("1.0", wiki_text)
    text.pack(expand=True, fill="both")
    root.mainloop()

# ---------------------------
# Main Terminal Menu
# ---------------------------
def menu():
    os.system("cls" if os.name == "nt" else 'clear')

    print("\n===== Tower Wiki Tool =====")
    print("1. Select tower file")
    print("2. Generate wiki page")
    print("3. Exit")
    print("")
    print("")
    print("")
    print(f"Selected File: {selected_File}")

    choice = input("Select option: ")

    if choice == "1":
        select_File()
    elif choice == "2":
        try:
            tower_data = load_lua_Table(selected_File)
            # Use filename (without extension) as tower name
            tower_name = os.path.splitext(os.path.basename(selected_File))[0]
            wiki_text = generate_tower_wiki(tower_name, tower_data)

            out_file = os.path.join("wiki", tower_name + ".txt")
            with open(out_file, "w", encoding="utf8") as f:
                f.write(wiki_text)
            menu()
            print("Convertion success")
        except Exception as e:
            print(f"Error processing {selected_File}: {e}")

    elif choice == "3":
        exit()

menu()