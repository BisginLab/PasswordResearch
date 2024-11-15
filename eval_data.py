from tqdm import tqdm

# Function to count matches in a given file
def count_matches(file_path, generated_password_set):
    match_count = 0
    total_count = 0
    matched_passwords = set()
    with open(file_path, 'r', encoding='latin-1') as f:
        for line in tqdm(f, desc=f"Checking passwords in {file_path}"):
            total_count += 1
            if line.strip() in generated_password_set:
                match_count += 1
                matched_passwords.add(line.strip())


    with open("matched_passwords.txt", 'w', encoding='latin-1') as output_file:
        for password in matched_passwords:
            output_file.write(password + '\n')
    return match_count, total_count

# Load generated passwords into a set
with open("generated_passwords.txt", 'r', encoding='latin-1') as f:
    generated_password_set = set(line.strip() for line in f)

# Count matches in test_data
test_matches, test_total = count_matches("test_data.txt", generated_password_set)



# Calculate percentages
test_percentage = (test_matches / test_total) * 100 if test_total > 0 else 0

# Print the results
print(f"Matches in test_data: {test_matches} ({test_percentage:.2f}%) out of {test_total}")



def count_matches_reverse(generated_file_path, test_file_path):
    
    with open(generated_file_path, 'r', encoding='latin-1') as f:
        generated_password_set = set(line.strip() for line in f)
        total_count = len(generated_password_set)

    match_count = 0
    found_password_set = set()

    # Process the large file in a memory-efficient way
    with open(test_file_path, 'r', encoding='latin-1') as f:
        for line in tqdm(f, desc=f"Checking passwords in {test_file_path}"):
            password = line.strip()
            if password in generated_password_set and password not in found_password_set:
                match_count += 1
                found_password_set.add(password)

    return match_count, total_count

# Count matches in hashcat_rockyou against test_rockyou
#hashcat_matches, hashcat_total = count_matches_reverse("test_rockyou.txt", "hashcat_rockyou.txt")

# Calculate percentage
#hashcat_percentage = (hashcat_matches / hashcat_total) * 100 if hashcat_total > 0 else 0

# Print the results
#print(f"Matches in hashcat_rockyou: {hashcat_matches} ({hashcat_percentage:.2f}%) out of {hashcat_total}")
