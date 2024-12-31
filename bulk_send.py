# bulk_send.py
from email_format import send_email, is_valid_email
import time

def timetaker(function):
    def inner(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        print(f"Function {function.__name__} took {(end - start):.2f} seconds.")
        return result
    return inner

@timetaker
def bulk_send():
    """Send emails in bulk with confirmation"""
    try:
        with open("emails.csv", 'r') as emails:
            for email in emails:
                email = email.strip()
                if not is_valid_email(email):
                    print(f"Skipping invalid email: {email}")
                    continue
                
                print(f"the email is {email}" )
                print(f"(Simulation) Email ready to be sent to {email}.")
                send_email(email)
                print(f"Email successfully sent to {email}.")

    except FileNotFoundError:
        print("Emails file not found. Ensure 'emails.csv' is in the correct location.")

if __name__ == "__main__":
    bulk_send()


