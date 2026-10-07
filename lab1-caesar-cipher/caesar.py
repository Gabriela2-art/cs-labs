ALPHABET = ["A", "Ă", "Â", "B", "C", "D", "E", "F", "G", "H", "I", "Î", "J",
            "K", "L", "M", "N", "O", "P", "Q", "R", "S", "Ș", "T", "Ț", "U",
            "V", "W", "X", "Y", "Z"]
N = len(ALPHABET)                                    
CODE = {letter: i for i, letter in enumerate(ALPHABET)}  

CEDILLA_FIX = {"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"}

MIN_KEY, MAX_KEY = 1, N - 1                         
MIN_KEYWORD_LEN = 7


def normalize(text):
    """Replace cedilla variants, convert to uppercase and remove spaces."""
    for wrong, right in CEDILLA_FIX.items():
        text = text.replace(wrong, right)
    return text.upper().replace(" ", "")


def find_invalid_char(text):
    """Return the first character that is not a Romanian letter, or None."""
    for ch in text:
        if ch not in CODE:
            return ch
    return None


def read_key():
    """Ask for the numeric key until an integer in 1..30 is entered."""
    while True:
        prompt = f"Enter key 1 (integer from {MIN_KEY} to {MAX_KEY}): "
        raw = input(prompt).strip()
        if raw.lstrip("-").isdigit() and MIN_KEY <= int(raw) <= MAX_KEY:
            return int(raw)
        print(f"  Error: '{raw}' is not a valid key. "
              f"The key must be an integer between {MIN_KEY} and {MAX_KEY}.")


def read_text(prompt):
    """Ask for a message until it contains only Romanian letters (and spaces)."""
    while True:
        text = normalize(input(prompt))
        bad = find_invalid_char(text)
        if text and bad is None:
            return text
        if not text:
            print("  Error: the text is empty. Enter at least one letter.")
        else:
            print(f"  Error: invalid character '{bad}'. Only letters of the "
                  "Romanian alphabet (A-Z, Ă, Â, Î, Ș, Ț, upper or lower case) "
                  "and spaces are allowed.")


def read_keyword():
    """Ask for key 2 until it has >= 7 characters, all Romanian letters."""
    while True:
        raw = input(f"Enter key 2 (keyword, Romanian letters only, "
                    f"at least {MIN_KEYWORD_LEN} characters): ")
        word = normalize(raw.strip())
        bad = find_invalid_char(word)
        if bad is not None or " " in raw.strip():
            bad = bad if bad is not None else " "
            print(f"  Error: invalid character '{bad}' in the keyword. "
                  "Only letters of the Romanian alphabet "
                  "(A-Z, Ă, Â, Î, Ș, Ț) are allowed.")
        elif len(word) < MIN_KEYWORD_LEN:
            print(f"  Error: the keyword has {len(word)} characters. It must "
                  f"contain at least {MIN_KEYWORD_LEN} letters.")
        else:
            return word

def build_permuted_alphabet(keyword):
    """Distinct letters of the keyword first, then the remaining letters in order."""
    result = []
    for letter in keyword + "".join(ALPHABET):
        if letter not in result:
            result.append(letter)
    return result


def shift(text, k, alphabet):
    """Replace each letter by the one k positions further in `alphabet` (mod n)."""
    n = len(alphabet)
    position = {letter: i for i, letter in enumerate(alphabet)}
    out = []
    for letter in text:
        x = position[letter]
        y = (x + k) % n
        if y < 0:                
            y += n
        out.append(alphabet[y])
    return "".join(out)


def encrypt(text, k, alphabet=ALPHABET):
    return shift(text, k, alphabet)          # c = (x + k) mod n


def decrypt(text, k, alphabet=ALPHABET):
    return shift(text, -k, alphabet)         # m = (y - k) mod n

def read_choice(prompt, allowed):
    while True:
        choice = input(prompt).strip().upper()
        if choice in allowed:
            return choice
        print(f"  Error: choose one of: {', '.join(allowed)}.")


def run_task(with_permutation):
    op = read_choice("Operation - (E)ncrypt or (D)ecrypt: ", ["E", "D"])
    k1 = read_key()
    alphabet = ALPHABET
    if with_permutation:
        keyword = read_keyword()
        alphabet = build_permuted_alphabet(keyword)
        print("Standard alphabet: " + " ".join(ALPHABET))
        print("Permuted alphabet: " + " ".join(alphabet))
    if op == "E":
        message = read_text("Enter the message: ")
        print(f"Message (prepared): {message}")
        print(f"Ciphertext:         {encrypt(message, k1, alphabet)}")
    else:
        cipher = read_text("Enter the ciphertext: ")
        print(f"Ciphertext:         {cipher}")
        print(f"Decrypted message:  {decrypt(cipher, k1, alphabet)}")


def main():
    while True:
        print("\n===== Caesar cipher (Romanian alphabet, n = 31) =====")
        print("1. Caesar cipher (Task 1.1)")
        print("2. Caesar cipher with a permutation (Task 1.2)")
        print("0. Exit")
        choice = read_choice("Your choice: ", ["1", "2", "0"])
        if choice == "0":
            break
        run_task(with_permutation=(choice == "2"))


if __name__ == "__main__":
    main()
