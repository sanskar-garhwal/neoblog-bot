import os
import requests
import smtplib
from email.mime.text import MIMEText
from random import choice

# Load environment variables from GitHub Secrets
HF_API_TOKEN = os.getenv('HF_API_TOKEN')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')

# Hugging Face API configuration
MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# Blog topics
topics = [
    "JEE and Competitive Exams: What You Need to Know",
    "JEE Preparation as an Indian Student: Tips and Real Talk",
    # ... rest of your topics ...
]

def generate_blog(prompt):
    """Generate blog content using Hugging Face API"""
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "No text generated.")
    except Exception as e:
        return f"Error generating blog: {str(e)}"

def send_email(subject, body):
    """Send email with generated blog content"""
    if not all([SENDER_EMAIL, RECEIVER_EMAIL, APP_PASSWORD]):
        print("Email configuration incomplete")
        return False

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully")
        return True
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False

def main():
    """Main execution flow"""
    # Validate all required environment variables
    if not all([HF_API_TOKEN, SENDER_EMAIL, RECEIVER_EMAIL, APP_PASSWORD]):
        print("Error: Missing required environment variables")
        return

    # Generate blog content
    topic = choice(topics)
    prompt = f"Write a creative, SEO-friendly blog post on: {topic}"
    print(f"Generating blog about: {topic}")
    
    blog_content = generate_blog(prompt)
    
    if not blog_content.startswith("Error"):
        print("Blog generated successfully")
        send_email(f"New Blog: {topic}", blog_content)
    else:
        print(blog_content)

if __name__ == "__main__":
    main()
