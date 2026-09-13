def not_empty(value):
    if value is None:
        return False
    return bool(str(value).strip())


def valid_email(email):
    if email is None:
        return False
    email = str(email).strip()
    if "@" not in email:
        return False
    local, domain = email.split("@", 1)
    return bool(local) and "." in domain and domain.split(".")[-1] != ""
