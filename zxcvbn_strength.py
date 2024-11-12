import zxcvbn
import csv
import tqdm
def process_password_file_zxcvbn(input_file, output_file):
    """
    Processes the input password file and calculates entropy using zxcvbn.
    Writes the results into an output CSV file.
    """
    with open(input_file, 'r') as f:
        passwords = f.readlines()

    print("Processing passwords with zxcvbn...")

    results = []
    for password in passwords:
        password = password.strip()
        if password:
            result = zxcvbn.zxcvbn(password)
            result['password'] = password  # Add password to the result dictionary
            results.append(result)

    # Extract field names from the first result
    fieldnames = results[0].keys()

    with open(output_file, 'w', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"Results have been written to {output_file}")

# Input and output file paths
input_file = 'password_list.txt'
output_file = 'password_zxcvbn.csv'

# Process the file and calculate entropy using zxcvbn
process_password_file_zxcvbn(input_file, output_file)

print(f"Results have been written to {output_file}")