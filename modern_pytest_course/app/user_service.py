import time


def send_email(to: str, subject: str) -> bool:
    # Imagine this sends a real email
    print(f"Email sent to {to} with subject '{subject}'")
    time.sleep(2)  # Simulate a delay in sending the email

    return True


def register_user(email: str) -> dict:
    # Side effect: calls an external dependency (send_email) which we want to avoid in tests
    
    email_sent = send_email(email, "Welcome!")
    if email_sent:
        return {"email": email, "status": "registered"}

    return {"email": email, "status": "email_failed"}
