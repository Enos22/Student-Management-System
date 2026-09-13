def not_empty(text):
    return text.strip() != ""


def valid_email(email):
    return "@" in email and "." in email.split("@")[-1]