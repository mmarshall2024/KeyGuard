
def verify_access(key, email):
    return key == "MASTER_KEY_123" and "@gmail.com" in email
