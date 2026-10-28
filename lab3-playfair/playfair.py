import sys

ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"        # 31 letters
MATRIX_ALPHABET = ALPHABET.replace("Â", "")          # 30 letters (Â -> Î)
ROWS, COLS = 5, 6
MIN_KEY_LENGTH = 7

CEDILLA = {"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"}

FILLER = "X"          # inserted between two equal letters of the same pair
FILLER_FOR_X = "Q"    # used when the doubled letter is X itself
DEFAULT_PAD = "Z"     # added at the end when the number of letters is odd

ALLOWED_HINT = ("Allowed characters: 'A'-'Z', 'a'-'z' and the Romanian letters "
                "Ă Â Î Ș Ț / ă â î ș ț (spaces are ignored).")

def normalize(text):
    """Removes spaces, converts to uppercase and checks the characters.
    Returns (letters, invalid_characters)."""
    letters, invalid = [], []
    for ch in text:
        if ch.isspace():
            continue
        ch = CEDILLA.get(ch, ch).upper()
        if ch in ALPHABET:
            letters.append("Î" if ch == "Â" else ch)
        elif ch not in invalid:
            invalid.append(ch)
    return "".join(letters), invalid


def prepare_key(key):
    """Removes the repeated letters of the key, starting with the second
    appearance of each letter (e.g. DUBLURA -> DUBLRA)."""
    result = ""
    for ch in key:
        if ch not in result:
            result += ch
    return result

def build_matrix(key):
    """Fills the matrix row by row: first the processed key, then the
    remaining letters of the alphabet in alphabetical order."""
    sequence = prepare_key(key)
    sequence += "".join(ch for ch in MATRIX_ALPHABET if ch not in sequence)
    matrix = [list(sequence[r * COLS:(r + 1) * COLS]) for r in range(ROWS)]
    position = {matrix[r][c]: (r, c) for r in range(ROWS) for c in range(COLS)}
    return matrix, position


def print_matrix(matrix):
    print("\nEncryption matrix (5 x 6):")
    for row in matrix:
        print("    " + "  ".join(row))

def filler_for(letter):
    return FILLER_FOR_X if letter == FILLER else FILLER


def prepare_text(letters, pad=DEFAULT_PAD):
    """Splits the text into pairs of letters. Between two equal letters of
    the same pair a filler is inserted; if the number of letters is odd,
    the additional letter chosen by the user is added at the end."""
    pairs, i = [], 0
    while i < len(letters):
        a = letters[i]
        if i + 1 < len(letters):
            b = letters[i + 1]
            if a == b:                     # double letter in the same pair
                pairs.append(a + filler_for(a))
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        else:                              # odd number of letters
            last = pad if pad != a else filler_for(a)
            pairs.append(a + last)
            i += 1
    return pairs

def transform_pair(pair, matrix, position, shift):
    """shift = +1 for encryption, -1 for decryption."""
    (r1, c1), (r2, c2) = position[pair[0]], position[pair[1]]
    if r1 == r2:                          # same row -> next/previous column
        rule = "same row"
        out = matrix[r1][(c1 + shift) % COLS] + matrix[r2][(c2 + shift) % COLS]
    elif c1 == c2:                        # same column -> next/previous row
        rule = "same column"
        out = matrix[(r1 + shift) % ROWS][c1] + matrix[(r2 + shift) % ROWS][c2]
    else:                                 # rectangle -> swap the columns
        rule = "rectangle"
        out = matrix[r1][c2] + matrix[r2][c1]
    return out, rule


def process(pairs, matrix, position, shift):
    results = []
    for p in pairs:
        out, rule = transform_pair(p, matrix, position, shift)
        results.append((p, rule, out))
    return results


def print_steps(results):
    print("\nPair   Rule          Result")
    for p, rule, out in results:
        print(f"  {p}   {rule:<12}  {out}")


def read_key():
    while True:
        key, invalid = normalize(input("Enter the key: "))
        if invalid:
            print("  Invalid characters:", " ".join(invalid))
            print("  " + ALLOWED_HINT)
        elif len(key) < MIN_KEY_LENGTH:
            print(f"  The key must contain at least {MIN_KEY_LENGTH} letters "
                  f"(you entered {len(key)}).")
        else:
            return key


def read_text(prompt):
    while True:
        text, invalid = normalize(input(prompt))
        if invalid:
            print("  Invalid characters:", " ".join(invalid))
            print("  " + ALLOWED_HINT)
        elif not text:
            print("  The text must contain at least one letter.")
        else:
            return text


def read_pad():
    while True:
        answer = input(f"Additional letter for an odd length "
                       f"(Enter = {DEFAULT_PAD}): ").strip()
        if not answer:
            return DEFAULT_PAD
        pad, invalid = normalize(answer)
        if len(pad) == 1 and not invalid:
            return pad
        print("  Enter exactly one letter. " + ALLOWED_HINT)


def read_cryptogram():
    while True:
        text = read_text("Enter the cryptogram: ")
        if len(text) % 2:
            print("  The cryptogram must contain an even number of letters.")
            continue
        pairs = [text[i:i + 2] for i in range(0, len(text), 2)]
        bad = [p for p in pairs if p[0] == p[1]]
        if bad:
            print("  A Playfair cryptogram cannot contain a pair of two equal "
                  "letters:", " ".join(bad))
            continue
        return pairs


def encrypt_dialog():
    key = read_key()
    matrix, position = build_matrix(key)
    letters = read_text("Enter the message: ")
    pad = read_pad()
    print("\nKey after removing repeated letters:", prepare_key(key))
    print_matrix(matrix)
    pairs = prepare_text(letters, pad)
    print("\nMessage prepared for encryption:")
    print("    " + " ".join(pairs))
    results = process(pairs, matrix, position, +1)
    print_steps(results)
    cipher = [out for _, _, out in results]
    print("\nCryptogram (pairs):", " ".join(cipher))
    print("Cryptogram:        ", "".join(cipher))


def decrypt_dialog():
    key = read_key()
    matrix, position = build_matrix(key)
    pairs = read_cryptogram()
    print("\nKey after removing repeated letters:", prepare_key(key))
    print_matrix(matrix)
    results = process(pairs, matrix, position, -1)
    print_steps(results)
    plain = [out for _, _, out in results]
    print("\nDecrypted message (pairs):", " ".join(plain))
    print("Decrypted message:        ", "".join(plain))
    print(f"(The fillers {FILLER}/{FILLER_FOR_X}, the final additional letter "
          "and the spaces are handled manually.)")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    print("PLAYFAIR CIPHER - Romanian alphabet (31 letters)")
    while True:
        print("\n1 - Encryption\n2 - Decryption\n0 - Exit")
        choice = input("Choose the operation: ").strip()
        if choice == "1":
            encrypt_dialog()
        elif choice == "2":
            decrypt_dialog()
        elif choice == "0":
            break
        else:
            print("  Choose 1, 2 or 0.")


if __name__ == "__main__":
    main()
