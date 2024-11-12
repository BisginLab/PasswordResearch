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
with open("generated_passwords2.txt", 'r', encoding='latin-1') as f:
    generated_password_set = set(line.strip() for line in f)

# Count matches in test_rockyou
test_rockyou_matches, test_rockyou_total = count_matches("test_rockyou.txt", generated_password_set)

# Count matches in test_rockyou_no_hc
#test_rockyou_no_hc_matches, test_rockyou_no_hc_total = count_matches("test_rockyou_no_hc.txt", generated_password_set)

# Calculate percentages
test_rockyou_percentage = (test_rockyou_matches / test_rockyou_total) * 100 if test_rockyou_total > 0 else 0
#test_rockyou_no_hc_percentage = (test_rockyou_no_hc_matches / test_rockyou_no_hc_total) * 100 if test_rockyou_no_hc_total > 0 else 0

# Print the results
print(f"Matches in test_rockyou: {test_rockyou_matches} ({test_rockyou_percentage:.2f}%) out of {test_rockyou_total}")
#print(f"Matches in test_rockyou_no_hc: {test_rockyou_no_hc_matches} ({test_rockyou_no_hc_percentage:.2f}%) out of {test_rockyou_no_hc_total}")



def count_matches_reverse(test_file_path, hashcat_file_path):
    # Load test_rockyou passwords into a set
    with open(test_file_path, 'r', encoding='latin-1') as f:
        test_password_set = set(line.strip() for line in f)
        total_count = len(test_password_set)

    match_count = 0
    found_password_set = set()

    # Process the large file in a memory-efficient way
    with open(hashcat_file_path, 'r', encoding='latin-1') as f:
        for line in tqdm(f, desc='Checking passwords in hashcat_rockyou'):
            password = line.strip()
            if password in test_password_set and password not in found_password_set:
                match_count += 1
                found_password_set.add(password)

    return match_count, total_count

# Count matches in hashcat_rockyou against test_rockyou
#hashcat_matches, hashcat_total = count_matches_reverse("test_rockyou.txt", "hashcat_rockyou.txt")

# Calculate percentage
#hashcat_percentage = (hashcat_matches / hashcat_total) * 100 if hashcat_total > 0 else 0

# Print the results
#print(f"Matches in hashcat_rockyou: {hashcat_matches} ({hashcat_percentage:.2f}%) out of {hashcat_total}")