def format_email(email):
    result = email.strip().lower()

    if "@" not in result:
        raise ValueError("Invalid email address")

    return result
