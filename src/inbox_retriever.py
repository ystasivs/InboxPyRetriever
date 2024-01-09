import imaplib
import email
from email.header import decode_header
from db_storage import DbStorage
from config import USER_EMAIL, PASSWORD
from datetime import datetime


def extract_body(msg):
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8")
                break
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8")

    return body


def get_emails(username, password):
    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)

    # Select the mailbox (inbox in this case)
    mail.select("inbox")

    # Get today's date in the required format
    today_date = datetime.now().strftime("%d-%b-%Y")

    # Search for emails sent on today's date
    result, data = mail.search(None, f'(SENTON "{today_date}")')

    # Retrieve email IDs from the search result
    email_ids = data[0].split()

    emails = []

    for email_id in email_ids:
        # Fetch the email data by ID
        result, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]

        # Parse the raw email data
        msg = email.message_from_bytes(raw_email)

        # Decode the subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        # Extract other relevant information as needed
        sender = msg.get("From")
        date_str = msg.get("Date")
        body = extract_body(msg)
        to_recipients = msg.get("To", "")
        cc_recipients = msg.get("Cc", "")
        bcc_recipients = msg.get("Bcc", "")
        # Add the email details to the list
        emails.append((
            int(email_id),
            subject,
            sender,
            body,
            date_str,
            to_recipients,
            cc_recipients,
            bcc_recipients,
        ))

    mail.logout()
    return emails


def inbox_retriever(event, content):
    with DbStorage() as storage:
        todays_emails = get_emails(USER_EMAIL, PASSWORD)
        print(f'retrieved {len(todays_emails)} emails')
        storage.save_to_db(todays_emails)


if __name__ == "__main__":
    if not USER_EMAIL or not PASSWORD:
        print('Set EMAIL_ADDRESS and PASSWORD')
        exit(1)
    inbox_retriever({}, {})
