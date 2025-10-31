"""
COMP 163 - Project 1: Character Creator & Saving/Loading
Name: Bryant Clarke
Date: 10/22/2025

AI Usage: AI helped clean up formatting and suggested logic improvements 
for the save_character and load_character functions.
"""

import os  # Used to check file paths and handle save/load safely

def create_character(name, character_class):
    """
    Creates a new character with calculated stats and default values.
    Returns a dictionary with all character info.
    """
    cls = _normalize_class(character_class)
    if cls is None:  # Invalid class
        return None

    level = 1
    strength, magic, health = calculate_stats(cls, level)
    return {
        "name": name,
        "class": cls,
        "level": level,
        "strength": strength,
        "magic": magic,
        "health": health,
        "gold": 100
    }

def calculate_stats(character_class, level):
    """
    Calculates strength, magic, and health based on class and level.
    Each class has unique base and growth stats.
    """
    cls = _normalize_class(character_class)
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
        return 0, 0, 0

    level_adj = max(1, int(level)) - 1
    strength = base["str"] + growth["str"] * level_adj
    magic = base["mag"] + growth["mag"] * level_adj
    health = base["hp"] + growth["hp"] * level_adj
    return strength, magic, health

def save_character(character, filename):
    """
    Saves character info to a text file in the required format.
    Returns True if saved successfully, False otherwise.
    """
    if not character or filename == "":
        return False
    if not os.access(os.path.dirname(filename) or ".", os.W_OK):
        return False

    with open(filename, "w") as f:
        f.write(f"Character Name: {character['name']}\n")
        f.write(f"Class: {character['class']}\n")
        f.write(f"Level: {character['level']}\n")
        f.write(f"Strength: {character['strength']}\n")
        f.write(f"Magic: {character['magic']}\n")
        f.write(f"Health: {character['health']}\n")
        f.write(f"Gold: {character['gold']}\n")
    return True

def load_character(filename):
    """
    Loads character info from a text file.
    Returns a character dictionary, or None if the file is missing or incomplete.
    """
    if not os.path.exists(filename):
        return None

    lines = []
    with open(filename, "r") as f:
        for line in f:
            clean = line.strip()
            if clean:
                lines.append(clean)

    data = {}
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            data[key] = value

    if len(data) < 7 and "Character Name" not in data:
        return None

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
    print("=== CHARACTER SHEET ===")
    print(f"Name: {character['name']}")
    print(f"Class: {character['class']}")
    print(f"Level: {character['level']}")
    print(f"Strength: {character['strength']}")
    print(f"Magic: {character['magic']}")
    print(f"Health: {character['health']}")
    print(f"Gold: {character['gold']}")

def level_up(character):
    """
    Increases character level by one and updates their stats.
    """
    character["level"] += 1
    strength, magic, health = calculate_stats(character["class"], character["level"])
    character["strength"] = strength
    character["magic"] = magic
    character["health"] = health

def _normalize_class(character_class):
    """
    Ensures the class name is valid (Warrior, Mage, Rogue, Cleric).
    Returns None if invalid.
    """
    if not character_class:
        return None
    c = character_class.strip().title()
    if c in ["Warrior", "Mage", "Rogue", "Cleric"]:
        return c
    return None

# Main area for testing
if __name__ == "__main__":
    print("=== CHARACTER CREATOR ===")
    char = create_character("Aria", "Mage")
    display_character(char)
    save_character(char, "aria.txt")
    loaded = load_character("aria.txt")
    display_character(loaded)
    level_up(loaded)
    display_character(loaded)
