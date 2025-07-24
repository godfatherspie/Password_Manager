import re
import random
from difflib import SequenceMatcher

def load_common_passwords(file_path="common_passwords.txt"):
    try:
        with open(file_path, "r") as f:
            return set(line.strip().lower() for line in f)
    except FileNotFoundError:
        return set()

def rule_based_score(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 10
    else:
        feedback.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 10
    else:
        feedback.append("Add uppercase letters")

    if re.search(r"[a-z]", password):
        score += 10
    else:
        feedback.append("Add lowercase letters")

    if re.search(r"\d", password):
        score += 10
    else:
        feedback.append("Include numbers")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 10
    else:
        feedback.append("Use special symbols (!@#$ etc.)")

    return score, feedback

def estimate_brute_force_time(password):
    charset_size = 0
    if re.search(r"[a-z]", password): charset_size += 26
    if re.search(r"[A-Z]", password): charset_size += 26
    if re.search(r"\d", password): charset_size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): charset_size += 32
    combinations = charset_size ** len(password)
    guesses_per_sec = 1_000_000_000
    seconds = combinations / guesses_per_sec
    return seconds

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds / 86400:.2f} days"
    else:
        return f"{seconds / 31536000:.2f} years"

def detect_dictionary_variants(password, dictionary):
    substitutions = {
        'a': ['@', '4'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['$', '5'],
        't': ['7']
    }

    password_lower = password.lower()

    for word in dictionary:
        if word in password_lower:
            return True

        modified = word
        for letter, subs in substitutions.items():
            for sub in subs:
                modified = modified.replace(letter, sub)

        if modified in password_lower:
            return True

        if SequenceMatcher(None, word, password_lower).ratio() > 0.85:
            return True

    return False

def evaluate_password(password, common_passwords):
    if detect_dictionary_variants(password, common_passwords):
        return {
            "label": "Very Weak",
            "score": 0,
            "time_to_crack": "Instant (dictionary-based guess)",
            "feedback": ["Password resembles a common word or pattern."]
        }

    score, feedback = rule_based_score(password)
    time_sec = estimate_brute_force_time(password)

    if score <= 20:
        label = "Weak"
    elif score <= 35:
        label = "Medium"
    elif score <= 45:
        label = "Strong"
    else:
        label = "Very Strong"

    return {
        "label": label,
        "score": score,
        "time_to_crack": format_time(time_sec),
        "feedback": feedback
    }

def generate_strong_password(length=12):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{};:,.<>/?"
    return ''.join(random.choice(chars) for _ in range(length))
