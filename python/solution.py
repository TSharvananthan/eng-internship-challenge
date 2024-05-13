from typing import List, Dict
from string import ascii_uppercase

def _generate_playfair_grid(keyword: str,
                            replace_j: bool = True) -> List[List[str]]:
    """ Generates a character grid for a Playfair encryption/decryption.

    Args:
        keyword (str): A keyword that represents the first few unique
        characters of a Playfair grid.
        replace_j (bool): If True, generate a Playfair grid where instances of
        "J" are replaced with "I"s.

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

    if replace_j:
        characters = list(ascii_uppercase.replace("J", "I"))
    else:
        characters = list(ascii_uppercase)

    for character in characters:
        if character in playfair_row:
            continue

        if len(playfair_row) == 5*5:
            break

        playfair_row.append(character)

    playfair_grid = [playfair_row[i: i+5]
                     for i in range(0, len(playfair_row), 5)]
    
    return playfair_grid

def _generate_position_map(lst: list) -> Dict[str, tuple]:
    """ Maps values of a 2D list to their respective postions.

    Args:
        lst (list): A non-empty 2D list.

    Returns:
        Dict[str, tuple]: A dictionary that maps values of the given 2D
        list to tuple (x, y).
    """
    position_map = {}

    for i, rows in enumerate(lst):
        for j, value in enumerate(rows):
            position_map[value] = (i, j)

    return position_map

def _generate_bigrams(message: str) -> List[str]:
    """ Generate bigrams from a message encrypted by the Playfair cipher.

    Args:
        message (str): A given message, most likely one from the Playfair
        cipher.

    Returns:
        List[str]: A list of two character bigrams. Note that repeated
        characters have an "X" inserted in between.
    """
    bigrams = [message[i: i+2] for i in range(0, len(message), 2)]

    for i, bigram in enumerate(bigrams):
        if len(set(bigram)) == 1:
            bigrams[i] = bigrams[0] + "X"

    return bigrams

def decrypt_playfair_cipher(encrypted_message: str, keyword: str) -> str:
    """ Decrypt a message encrypted by the Playfair cipher.

    Args:
        encrypted_message (str): An encrypted message.
        keyword (str): A phrase that represents the first few unique
        characters of a Playfair grid.

    Returns:
        str: A decrypted message.
    """

    playfair_grid = _generate_playfair_grid(keyword)
    position_map = _generate_position_map(playfair_grid)
    encrypted_bigrams = _generate_bigrams(encrypted_message)

    decrypted_bigrams = []

    for encrypted_bigram in encrypted_bigrams:
        c1, c2 = encrypted_bigram

        c1_row, c1_col = position_map[c1]
        c2_row, c2_col = position_map[c2]

        if c1_row == c2_row:
            first_char_decrypt = playfair_grid[c1_row][(c1_col - 1) % 5]
            second_char_decrypt = playfair_grid[c2_row][(c2_col - 1) % 5]

        elif c1_col == c2_col:
            first_char_decrypt = playfair_grid[(c1_row - 1) % 5][c1_col]
            second_char_decrypt = playfair_grid[(c2_row - 1) % 5][c2_col]
        
        else:
            first_char_decrypt = playfair_grid[c1_row][c2_col]
            second_char_decrypt = playfair_grid[c2_row][c1_col]

        decrypted_bigram = first_char_decrypt + second_char_decrypt
        decrypted_bigrams.append(decrypted_bigram)

        decrypted_message = "".join(decrypted_bigrams)

    return decrypted_message

if __name__ == "__main__":
    encrypted_message = "IKEWENENXLNQLPZSLERUMRHEERYBOFNEINCHCV"
    key = "SUPERSPY"
    playfair_grid = _generate_playfair_grid(encrypted_message)
    decrypted_message = decrypt_playfair_cipher(encrypted_message, key)
    print(decrypted_message)