from typing import List
from string import ascii_uppercase

def _generate_playfair_grid(keyword: str) -> List[List[str]]:
    """ Generates a character grid for a Playfair encryption/decryption.

    Args:
        keyword (str): A keyword that represents the first few unique
        characters of a Playfair grid.

    Returns:
        List[List[str]]: A 2D list of uppercase characters, initially
        ordered by the unique characters of the keyword, then the remaining
        letters of the alphabet.
    """
    playfair_row = []

    for char in keyword:
        if char in playfair_row:
            continue

        playfair_row.append(char)

    characters = list(ascii_uppercase.replace("J", "I"))

    for character in characters:
        if character in playfair_row:
            continue

        if len(playfair_row) == 5*5:
            break

        playfair_row.append(character)

    playfair_grid = [playfair_row[i: i+5]
                     for i in range(0, len(playfair_row), 5)]
    
    return playfair_grid
