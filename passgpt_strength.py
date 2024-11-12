import torch
import numpy as np
from transformers import GPT2LMHeadModel, RobertaTokenizerFast
from tqdm import tqdm
import statistics

# Load PassGPT model and tokenizer
MAX_CHARS = 10

tokenizer = RobertaTokenizerFast.from_pretrained(
    "javirandor/passgpt-10characters",
    max_len=MAX_CHARS + 2,  # Max length + start and end tokens
    padding="max_length",
    truncation=True,
    do_lower_case=False,
    strip_accents=False,
    mask_token="<mask>",
    unk_token="<unk>",
    pad_token="<pad>",
    truncation_side="right"
)

model = GPT2LMHeadModel.from_pretrained("javirandor/passgpt-10characters").eval()


def calculate_log_prob_and_entropy(password, model, tokenizer):
    inputs = tokenizer(password, return_tensors='pt')
    input_ids = inputs['input_ids']

    # Get model output (logits)
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        logits = outputs.logits

    # Softmax to get probabilities
    probs = torch.softmax(logits, dim=-1)

    # Initialize log probability and entropy
    total_log_prob = 0
    total_entropy = 0

    for i in range(len(password)):
        # Get the probability distribution over the vocabulary for the current character position
        char_probs = probs[0, i, :].detach().cpu().numpy()

        # Log probability for the correct character
        char_id = input_ids[0][i].item()
        prob_correct_char = char_probs[char_id]
        log_prob = np.log10(prob_correct_char)
        total_log_prob += log_prob

        # Entropy calculation: Sum over all possible characters for the position
        position_entropy = -np.sum([p * np.log2(p) for p in char_probs if p > 0])
        total_entropy += position_entropy

    return total_log_prob, total_entropy

def calculate_statistics(passwords, model, tokenizer):
    log_probs = []
    entropies = []

    for password in tqdm(passwords, desc="Calculating statistics"):
        log_prob, entropy = calculate_log_prob_and_entropy(password, model, tokenizer)
        log_probs.append(log_prob)
        entropies.append(entropy)

    stats = {
        "log_prob_mean": statistics.mean(log_probs),
        "log_prob_variance": statistics.variance(log_probs),
        "log_prob_median": statistics.median(log_probs),
        "log_prob_stdev": statistics.stdev(log_probs),
        "entropy_mean": statistics.mean(entropies),
        "entropy_variance": statistics.variance(entropies),
        "entropy_median": statistics.median(entropies),
        "entropy_stdev": statistics.stdev(entropies)
    }

    return stats

def process_password_file(input_file, model, tokenizer):
    with open(input_file, 'r', encoding='latin-1') as f:
        passwords = [line.strip() for line in f if line.strip()]

    return calculate_statistics(passwords, model, tokenizer)

# Process the files and calculate statistics
cracked_stats = process_password_file('../cracked_passwords2.txt', model, tokenizer)
uncracked_stats = process_password_file('../uncracked_passwords2.txt', model, tokenizer)

# Print the results
print("Statistics for cracked_passwords:")
for key, value in cracked_stats.items():
    print(f"{key}: {value}")

print("\nStatistics for uncracked_passwords:")
for key, value in uncracked_stats.items():
    print(f"{key}: {value}")

