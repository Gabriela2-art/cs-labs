import secrets
import string

PC1_TABLE = [
    [57, 49, 41, 33, 25, 17, 9],
    [1, 58, 50, 42, 34, 26, 18],
    [10, 2, 59, 51, 43, 35, 27],
    [19, 11, 3, 60, 52, 44, 36],
    [63, 55, 47, 39, 31, 23, 15],
    [7, 62, 54, 46, 38, 30, 22],
    [14, 6, 61, 53, 45, 37, 29],
    [21, 13, 5, 28, 20, 12, 4],
]


def validate_ascii_key(key: str) -> tuple[bool, str]:
    """Return whether key is exactly eight ASCII characters."""
    if len(key) != 8:
        return False, "The key must contain exactly 8 characters."
    if any(ord(character) > 127 for character in key):
        return False, "Every character must be an ASCII character (0-127)."
    return True, ""


def generate_random_key() -> str:
    """Generate an eight-character printable ASCII key."""
    printable_ascii = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(printable_ascii) for _ in range(8))


def ascii_to_binary(key: str) -> tuple[list[int], str]:
    """Convert each ASCII character to eight bits and return the complete key."""
    character_bits = [format(ord(character), "08b") for character in key]
    return character_bits, "".join(character_bits)


def hex_to_binary(hex_key: str) -> str:
    """Convert a 16-digit hexadecimal DES key to exactly 64 bits."""
    return bin(int(hex_key, 16))[2:].zfill(64)


def pc1_permutation(key_bits: str) -> tuple[str, list[tuple[int, int]]]:
    """Apply PC-1 and record (output position, source position) selections."""
    selections = [
        (output_position, source_position)
        for output_position, source_position in enumerate(
            (position for row in PC1_TABLE for position in row), start=1
        )
    ]
    k_plus = "".join(key_bits[source_position - 1] for _, source_position in selections)
    return k_plus, selections


def format_bits(bits: str, group_size: int = 8) -> str:
    """Group a binary string to make it easier to read."""
    return " ".join(
        bits[index:index + group_size] for index in range(0, len(bits), group_size)
    )


def display_pc1_table() -> None:
    """Print the complete eight-by-seven PC-1 table."""
    print("\nPC-1 permutation table (1-based DES bit positions):")
    for row in PC1_TABLE:
        print("  " + " ".join(f"{position:2}" for position in row))


def display_selections(key_bits: str, selections: list[tuple[int, int]]) -> None:
    """Print how every K+ bit is selected from the original key."""
    print("\nPC-1 selections (K+ output bit <- original key bit):")
    for start in range(0, len(selections), 8):
        selected_group = selections[start:start + 8]
        details = []
        for output_position, source_position in selected_group:
            details.append(
                f"K+[{output_position:2}] <- key[{source_position:2}] = "
                f"{key_bits[source_position - 1]}"
            )
        print("  " + " | ".join(details))


def display_result(
    original_key: str,
    key_bits: str,
    k_plus: str,
    selections: list[tuple[int, int]],
    character_bits: list[str] | None = None,
    character_values: list[int] | None = None,
) -> None:
    """Display all intermediate values required by the laboratory task."""
    print("\n" + "=" * 78)
    print("DES TASK 2.1: INITIAL KEY PERMUTATION (PC-1)")
    print("=" * 78)
    print(f"Original key: {original_key}")

    if character_values is not None and character_bits is not None:
        print("\nASCII values and 8-bit binary representations:")
        for index, (character, value, bits) in enumerate(
            zip(original_key, character_values, character_bits), start=1
        ):
            print(f"  Character {index}: {character!r}  ASCII {value:3}  binary {bits}")
    else:
        print("Input type: standard 16-digit hexadecimal DES test vector")

    print(f"\nOriginal key, 64 bits: {format_bits(key_bits)}")
    print(f"Bit count: {len(key_bits)}")
    display_pc1_table()
    display_selections(key_bits, selections)
    print(f"\nK+ (56 bits): {format_bits(k_plus)}")
    print(f"Bit count: {len(k_plus)}")
    print(f"C0 (first 28 bits): {format_bits(k_plus[:28], 7)}")
    print(f"D0 (last 28 bits):  {format_bits(k_plus[28:], 7)}")
    print("=" * 78)


def process_ascii_key(key: str) -> bool:
    """Validate, convert, permute, and display an ASCII key."""
    is_valid, error_message = validate_ascii_key(key)
    if not is_valid:
        print(f"Error: {error_message}")
        return False

    character_bits, key_bits = ascii_to_binary(key)
    k_plus, selections = pc1_permutation(key_bits)
    display_result(
        key,
        key_bits,
        k_plus,
        selections,
        character_bits,
        [ord(character) for character in key],
    )
    return True


def run_standard_test_vector() -> None:
    """Run the well-known DES PC-1 verification vector."""
    hex_key = "133457799BBCDFF1"
    key_bits = hex_to_binary(hex_key)
    k_plus, selections = pc1_permutation(key_bits)
    expected_k_plus = "11110000110011001010101011110101010101100110011110001111"
    display_result(hex_key, key_bits, k_plus, selections)
    print(f"\nExpected K+ for this vector: {format_bits(expected_k_plus)}")
    print(f"Verification: {'PASS' if k_plus == expected_k_plus else 'FAIL'}")


def main() -> None:
    """Run the interactive console menu."""
    while True:
        print("\nDES Task 2.1 - Determine K+ using PC-1")
        print("1. Enter an 8-character ASCII key")
        print("2. Generate a random 8-character ASCII key")
        print("3. Run the standard DES hexadecimal test vector")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            process_ascii_key(input("Enter exactly 8 ASCII characters: "))
        elif choice == "2":
            key = generate_random_key()
            print(f"Generated key: {key}")
            process_ascii_key(key)
        elif choice == "3":
            run_standard_test_vector()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Error: choose 0, 1, 2, or 3.")


if __name__ == "__main__":
    main()
