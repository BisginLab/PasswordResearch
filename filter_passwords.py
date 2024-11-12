from tqdm import tqdm

def filter_hibp():
    # Open input and output files
    with open("./passgpt/filtered_hibp.txt", "r") as infile, open("./passgpt/filtered_hibp_new.txt", "w") as outfile:
        count = 0
        lines = infile.readlines()
        for line in tqdm(lines, desc="Filtering passwords"):
            password = line.strip()
            # Write passwords with length <= 16 to the output file
            if len(password) <= 10:
                outfile.write(password + "\n")
                count += 1

    print(count)

def filter_rockyou():
    unique_passwords = set()

    with open("./passgpt/rockyou.txt", "r", encoding="latin-1") as infile:
        lines = infile.readlines()
        for line in tqdm(lines, desc="Filtering passwords"):
            password = line.strip()
            if len(password) <= 10:
                unique_passwords.add(password)

    with open("./passgpt/filtered_rockyou.txt", "w", encoding="latin-1") as outfile:
        for password in tqdm(unique_passwords, desc="Writing Unique Passwords"):
            outfile.write(password + "\n")


def remove_hc():
    # Read passwords from hashcat_rockyou
    with open("./hashcat_rockyou.txt", "r", encoding="latin-1") as infile1:
        hashcat_passwords = set()
        for line in tqdm(infile1, desc="Reading passwords"):
            hashcat_passwords.add(line.strip())

    # Read passwords from test_rockyou
    with open("./generated_passwords.txt", "r", encoding="latin-1") as infile2:
        generated_passwords = set(line.strip() for line in infile2.readlines())

    # Filter out passwords that are in hashcat_rockyou
    uncracked_passwords = []
    cracked_passwords = []
    for pwd in tqdm(generated_passwords, desc="Filtering passwords"):
        if pwd not in hashcat_passwords:
            uncracked_passwords.append(pwd)
        else:
            cracked_passwords.append(pwd)

    # Write the filtered passwords back to test_rockyou
    with open("./generated_uncracked.txt", "w", encoding="latin-1") as f:
        for pwd in uncracked_passwords:
            f.write(pwd + "\n")

    # Write the cracked passwords to a separate file
    with open("./generated_cracked.txt", "w", encoding="latin-1") as f:
        for pwd in cracked_passwords:
            f.write(pwd + "\n")

    print(f"{len(uncracked_passwords)} uncracked passwords and {len(cracked_passwords)} cracked passwords.")

def filter_xato():
    unique_passwords = set()

    with open("xato-net-10-million-passwords.txt", "r") as infile:
        lines = infile.readlines()
        full_count = len(lines)
        for line in tqdm(lines, desc="Filtering passwords"):
            password = line.strip()
            if len(password) <= 10:
                unique_passwords.add(password)

        filtered_count = len(unique_passwords)

    with open("filtered_xato.txt", "w") as outfile:
        for password in tqdm(unique_passwords, desc="Writing Unique Passwords"):
            outfile.write(password + "\n")

    print(f"Filtered {filtered_count} out of {full_count} passwords.")


def count_password_matches():
    # Load the smaller list of 100,000 passwords into memory as a set for quick lookup
    with open("generated_passwords.txt", 'r', encoding='latin-1') as f:
        generated_password_set = set(line.strip() for line in f)

    # Initialize counters
    match_count = 0
    non_match_count = len(generated_password_set)  # Initially set non-matches to the total in small list

    # Create a set to track already found passwords to avoid double-counting due to duplicates
    found_passwords = set()

    # Process the large file in a memory-efficient way
    with open("hashcat_rockyou.txt", 'r', encoding='latin-1') as f:
        for line in tqdm(f, desc="Checking passwords"):
            password = line.strip()
            # Check if the password is in the smaller set and hasn't been counted yet
            if password in generated_password_set and password not in found_passwords:
                match_count += 1
                non_match_count -= 1
                found_passwords.add(password)  # Mark this password as found

    # Return the results
    print("Passwords cracked:", match_count)
    print("Passwords not cracked:", non_match_count)


def remove_hc_2():
    # Load the smaller list of 100,000 passwords into memory as a set for quick lookup
    with open("test_rockyou.txt", 'r', encoding='latin-1') as f:
        test_set = set(line.strip() for line in f)

    # Process the large file in a memory-efficient way
    with open("hashcat_rockyou.txt", 'r', encoding='latin-1') as f:
        for line in tqdm(f, desc="Checking passwords"):
            password = line.strip()

            if password in test_set:
                test_set.remove(password)

    # Write the remaining passwords back to the file
    with open("test_rockyou_no_hc.txt", 'w', encoding='latin-1') as f:
        for password in tqdm(test_set, desc="Writing passwords"):
            f.write(password + "\n")

def split_cracked():
    # Load the smaller list of 100,000 passwords into memory as a set for quick lookup
    with open('generated_passwords2.txt', 'r', encoding='latin-1') as f:
        generated_password_set = set(line.strip() for line in f)

    # Initialize counters
    match_count = 0
    non_match_count = len(generated_password_set)  # Initially set non-matches to the total in small list

    # Create a set to track already found passwords to avoid double-counting due to duplicates
    found_passwords = set()

    # Open files to write cracked and uncracked passwords
    with open('cracked_passwords2.txt', 'w', encoding='latin-1') as cracked_file, \
         open('uncracked_passwords2.txt', 'w', encoding='latin-1') as uncracked_file:

        # Process the large file in a memory-efficient way
        with open('hashcat_rockyou.txt', 'r', encoding='latin-1') as f:
            for line in tqdm(f, desc='Checking passwords'):
                password = line.strip()
                # Check if the password is in the smaller set and hasn't been counted yet
                if password in generated_password_set and password not in found_passwords:
                    match_count += 1
                    non_match_count -= 1
                    found_passwords.add(password)  # Mark this password as found
                    generated_password_set.remove(password)  # Remove from the set to avoid duplicates
                    cracked_file.write(password + '\n')  # Write to cracked passwords file

        for password in tqdm(generated_password_set, desc='Writing uncracked passwords'):
            uncracked_file.write(password + '\n')

    # Return the results
    print('Passwords cracked:', match_count)
    print('Passwords not cracked:', non_match_count)

#split_cracked()

def count_unique():
    unique_passwords = set()

    with open("generated_passwords2.txt", "r", encoding="latin-1") as infile:
        lines = infile.readlines()
        for line in tqdm(lines, desc="Counting unique passwords"):
            password = line.strip()
            unique_passwords.add(password)

    print(len(unique_passwords))
    print(len(lines))
    print(len(unique_passwords) / len(lines) * 100)

#count_unique()