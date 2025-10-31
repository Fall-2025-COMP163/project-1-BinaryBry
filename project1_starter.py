"""
COMP 163 - Project 1: Character Creator & Saving/Loading
Name: Bryant Clarke
Date: 10/22/2025

AI Usage: AI helped clean up formatting and suggested logic improvements 
for the save_character and load_character functions, also helped with comments.
"""

import os  # I used os so I can safely check and manage file paths during saving/loading.

def create_character(name, character_class):
    """
    Creates a new character with calculated stats and default values.
    Returns a dictionary with all character info.
    """
    cls = _normalize_class(character_class)  # Makes sure the class name is valid and formatted right.
    if cls is None:  # I added this to stop invalid class inputs before they cause errors.
        return None

    level = 1  # All characters start at level 1.
    # I used calculate_stats() to get base stats right away when the character is made.
    strength, magic, health = calculate_stats(cls, level)
    # I stored all info in a dictionary so it's easy to access and save later.
    return {
        "name": name,
        "class": cls,
        "level": level,
        "strength": strength,
        "magic": magic,
        "health": health,
        "gold": 100  # Everyone starts with 100 gold — just like an RPG starting amount.
    }

def calculate_stats(character_class, level):
    """
    Calculates strength, magic, and health based on class and level.
    Each class has unique base and growth stats.
    """
    cls = _normalize_class(character_class)  # I reused normalization for consistency.
    
    # Each class has a base stat (starting power) and growth rate (how much stats go up each level).
    if cls == "Warrior":
        base = {"str": 14, "mag": 3, "hp": 120}
        growth = {"str": 4, "mag": 1, "hp": 12}
    elif cls == "Mage":
        base = {"str": 5, "mag": 15, "hp": 80}
        growth = {"str": 2, "mag": 4, "hp": 8}
    elif cls == "Rogue":
        base = {"str": 10, "mag": 8, "hp": 70}
        growth = {"str": 3, "mag": 2, "hp": 6}
    elif cls == "Cleric":
        base = {"str": 8, "mag": 14, "hp": 110}
        growth = {"str": 2, "mag": 4, "hp": 10}
    else:
        return 0, 0, 0  # I added this fallback so invalid classes don’t crash anything.

    level_adj = max(1, int(level)) - 1  # I used max() to keep levels from dropping below 1.
    # Each line here scales the stats using the level and growth rate.
    strength = base["str"] + growth["str"] * level_adj
    magic = base["mag"] + growth["mag"] * level_adj
    health = base["hp"] + growth["hp"] * level_adj
    return strength, magic, health  # Returns all three together as a tuple.

def save_character(character, filename):
    """
    Saves character info to a text file in the required format.
    Returns True if saved successfully, False otherwise.
    """
    # I used these checks to make sure the data and file name are valid.
    if not character or filename == "":
        return False
    # I used os.access() to make sure we actually have permission to write there.
    if not os.access(os.path.dirname(filename) or ".", os.W_OK):
        return False

    # I used "with open" so the file automatically closes after saving.
    with open(filename, "w") as f:
        # Each line writes one piece of data with a label for readability.
        f.write(f"Character Name: {character['name']}\n")
        f.write(f"Class: {character['class']}\n")
        f.write(f"Level: {character['level']}\n")
        f.write(f"Strength: {character['strength']}\n")
        f.write(f"Magic: {character['magic']}\n")
        f.write(f"Health: {character['health']}\n")
        f.write(f"Gold: {character['gold']}\n")
    return True  # Returns True if everything saves correctly.

def load_character(filename):
    """
    Loads character info from a text file.
    Returns a character dictionary, or None if the file is missing or incomplete.
    """
    # This check prevents the program from crashing if the file doesn’t exist.
    if not os.path.exists(filename):
        return None

    lines = []  # I used a list to store all the lines from the file.
    with open(filename, "r") as f:
        for line in f:
            clean = line.strip()  # I used strip() to remove blank spaces and newlines.
            if clean:
                lines.append(clean)

    data = {}  # I used a dictionary to match each label to its value.
    for line in lines:
        if ": " in line:  # Splits "Label: Value" into key and value pairs.
            key, value = line.split(": ", 1)
            data[key] = value

    # If the data is missing or incomplete, return None safely.
    if len(data) < 7 and "Character Name" not in data:
        return None

    # Converts numbers back to integers so calculations work later.
    return {
        "name": data["Character Name"],
        "class": _normalize_class(data["Class"]),
        "level": int(data["Level"]),
        "strength": int(data["Strength"]),
        "magic": int(data["Magic"]),
        "health": int(data["Health"]),
        "gold": int(data["Gold"])
    }

def display_character(character):
    """
    Prints the character sheet in a formatted way.
    Does not return anything.
    """
    # I used print statements to create a clean, readable character summary.
    print("=== CHARACTER SHEET ===")
    print(f"Name: {character['name']}")
    print(f"Class: {character['class']}")
    print(f"Level: {character['level']}")
