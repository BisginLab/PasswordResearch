from tqdm import tqdm
import binascii


def remove_hex():
# Open input and output files
    with open("315.100.found", "r") as infile, open("hibp.txt", "w") as outfile:
        lines = infile.readlines()
        for line in tqdm(lines, desc="Processing lines"):
            # Split by colon to separate the ID/hash from the content
            try:
                prefix, content = line.strip().split(":", 1)
                # Skip lines with hex encoding
                if content.startswith("$HEX["):
                    continue
                # Write plain text content to output file
                outfile.write(content + "\n")
            except ValueError:
                # Skip lines that don't match the expected format
                print(f"Skipping malformed line: {line.strip()}")


def count_hex_and_others():
    hex_long_count = 0
    hex_short_count = 0
    plain_long_count = 0
    plain_short_count = 0

    with open("315.100.found", "r") as infile, open("hex_shor.txt", "w") as outfile:
        lines = infile.readlines()
        for line in tqdm(lines, desc="Counting Lines"):
            try:
                prefix, content = line.strip().split(":", 1)
                if content.startswith("$HEX["):
                    # Convert HEX to plain text
                    hex_content = content[5:-1]  # Remove $HEX[ and ]
                    plain_text = binascii.unhexlify(hex_content).decode('utf-8', errors='ignore')
                    if len(plain_text) > 16:
                        hex_long_count += 1
                    else:
                        hex_short_count += 1
                        outfile.write(plain_text + "\n")
                else:
                    if len(content) > 16:
                        plain_long_count += 1
                    else:
                        plain_short_count += 1
            except ValueError:
                print(f"Skipping malformed line: {line.strip()}")

    print(f"HEX format longer than 16 characters: {hex_long_count}")
    print(f"HEX format shorter or equal to 16 characters: {hex_short_count}")
    print(f"Plain text format longer than 16 characters: {plain_long_count}")
    print(f"Plain text format shorter or equal to 16 characters: {plain_short_count}")

count_hex_and_others()