import os
import re
import requests
from html import unescape
from dotenv import load_dotenv
from openai import OpenAI
from zetect_auth import get_token
import json

GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages"


load_dotenv("zetect.env")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your zetect.env file.")

client = OpenAI(api_key=api_key)


def html_to_text(html):
    """Convert email HTML body into readable plain text."""
    if not html:
        return ""

    html = re.sub(r"(?i)</(p|div|br|li|h[1-6])>", "\n", html)
    html = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", html)
    text = re.sub(r"(?s)<[^>]+>", "", html)
    text = unescape(text)

    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    return text


def fetch_messages(token, top=10):
    """Fetch the 10 most recent inbox emails with sender, subject, date, and body."""
    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "$top": top,
        "$orderby": "receivedDateTime desc",
        "$select": "id,subject,from,receivedDateTime,body"
    }

    response = requests.get(
        GRAPH_API_ENDPOINT,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()
    return response.json().get("value", [])


def classify_with_gpt(sender, subject, body_text):
    """Send sender, subject, and body to GPT for phishing classification."""
    try:
        with open("gpt_prompt.txt", "r", encoding="utf-8") as f:
            base_prompt = f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError("gpt_prompt.txt not found.")

    prompt = (
        f"{base_prompt}\n\n"
        f"--- EMAIL TO ANALYZE ---\n"
        f"Sender: {sender}\n"
        f"Subject: {subject}\n\n"
        f"Body:\n{body_text[:2500]}\n\n"
        f"Return only the classification and one concise reason."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=180
    )

    return response.choices[0].message.content.strip()


def print_email_result(index, sender, subject, date, preview, ai_analysis):
    """Print one email and its GPT analysis in a readable terminal format."""
    print("\n" + "=" * 80)
    print(f"Email {index}")
    print("=" * 80)

    print(f"From: {sender}")
    print(f"Received: {date}")
    print(f"Subject: {subject}")
    print(f"Preview: {preview}")
    print("\nAI Analysis:")
    print(ai_analysis)

def saveEmails(index, sender, subject, date, preview, ai_analysis):
    data = {
        'Email': index,
        'Sender': sender,
        'Received': date,
        'Subject': subject,
        "Preview": preview,
        "AI analysis": ai_analysis
    }
    try:
        with open("emails.json", "r") as e:
            emails = json.load(e)
    except (FileNotFoundError, json.JSONDecodeError):
        emails = []  # start fresh if file is empty or broken

    emails.append({index: data})

    with open("emails.json", "w") as e:
        json.dump(emails, e, indent=4)
def main():
    """Fetch recent emails, analyze them with GPT, and print results."""
    token = get_token()
    messages = fetch_messages(token, top=10)

    if not messages:
        print("No emails found.")
        return

    print(f"\nZetect analyzed {len(messages)} recent emails.\n")

    for i, message in enumerate(messages, start=1):
        try:
            subject = message.get("subject") or "(no subject)"

            sender_dict = message.get("from", {}).get("emailAddress", {})
            sender = sender_dict.get("address", "(unknown)")

            date = message.get("receivedDateTime", "(unknown date)")

            body_obj = message.get("body") or {}
            body_html = body_obj.get("content") or ""
            body_text = html_to_text(body_html)

            preview = body_text[:240].replace("\n", " ").strip()
            if len(body_text) > 240:
                preview += "..."

            ai_analysis = classify_with_gpt(sender, subject, body_text)

            emails= {}
            saveEmails(
                index=i,
                sender=sender,
                subject=subject,
                date=date,
                preview=preview,
                ai_analysis=ai_analysis
            )

        except Exception as e:
            print(f"\nError processing email {i}: {e}")


if __name__ == "__main__":
    main()
