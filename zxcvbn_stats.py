import zxcvbn
import statistics
from tqdm import tqdm

def calculate_password_statistics(input_file):
    """
    Calculates statistics for zxcvbn scores of passwords in the input file.
    """
    with open(input_file, 'r', encoding="latin-1") as f:
        passwords = f.readlines()

    scores = []
    score_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for password in tqdm(passwords, desc="Calculating zxcvbn scores"):
        password = password.strip()
        if password:
            result = zxcvbn.zxcvbn(password)
            scores.append(result['score'])
            score_counts[result['score']] += 1

    mean_score = statistics.mean(scores)
    variance_score = statistics.variance(scores)
    median_score = statistics.median(scores)
    stdev_score = statistics.stdev(scores)

    print(f"{input_file}:")
    print(f"Number of passwords: {len(scores)}")
    print(f"Mean zxcvbn score: {mean_score}")
    print(f"Variance of zxcvbn scores: {variance_score}")
    print(f"Median zxcvbn score: {median_score}")
    print(f"Standard deviation of zxcvbn scores: {stdev_score}")
    for score, count in score_counts.items():
        print(f"Score {score}: {count}")

# Input file path
input_file = '../test_rockyou.txt'

# Calculate and print statistics
calculate_password_statistics(input_file)