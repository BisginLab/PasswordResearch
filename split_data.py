from sklearn.model_selection import train_test_split

# Path to your password dataset
input_file = "./passgpt/filtered_hibp_new.txt"

# Read passwords from file
with open(input_file, "r") as f:
    passwords = [line.strip() for line in f.readlines()]

# Split dataset
train_passwords, test_passwords = train_test_split(passwords, test_size=0.2, random_state=42)

# Write the training and test data to files
with open("./train_hibp.txt", "w") as train_file:
    for pwd in train_passwords:
        train_file.write(pwd + "\n")

with open("./test_hibp.txt", "w") as test_file:
    for pwd in test_passwords:
        test_file.write(pwd + "\n")

print("Data split into train and test sets.")

