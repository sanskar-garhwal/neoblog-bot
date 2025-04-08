import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from random import choice

# Environment variables for secrets
API_TOKEN = os.getenv("HF_API_TOKEN")
SENDER_EMAIL = os.getenv("GMAIL_SENDER")
RECEIVER_EMAIL = os.getenv("GMAIL_RECEIVER")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Blog topics
topics = [
    "JEE and Competitive Exams: What You Need to Know",
    "JEE Preparation as an Indian Student: Tips and Real Talk",
    "How to Earn Online as a Teen/Student in 2025",
    "All You Need to Know About AI in Daily Life",
    "How to Become an Influencer from Scratch",
    "Pressure on Indian Students: A Deep Dive",
    "Real Darknet Experiences: What You Should Know",
    "Life in India: The Beautiful Chaos",
    "What Is Quality Education and Why Does It Matter?",
    "Why Being a Student in India Is Tough But Worth It",
    "Mental Health and Burnout in Indian Education",
    "Passive Income Ideas for Students",
    "How Social Media Affects Student Life",
    "Top Free Tools Every Student Should Use in 2025",
    "From IIT Dreams to Reality: A JEE Topper’s Story",
    "Is AI Taking Over Jobs? What Students Should Know",
    "Smartphone Addiction and How to Beat It",
    "Freelancing as a Student: Where to Start",
    "School vs. Real Life: Skills They Don’t Teach",
    "What the Education System Can Learn from Finland",
    "How to Stay Motivated During Exam Season",
    "The Truth About Coaching Institutes in India",
    "College Life vs. School Life in India",
    "How to Build a Personal Brand as a Student"
]

# Pick a random topic
topic = choice(topics)
prompt = f"Write a creative, SEO-friendly and human-like blog post on the topic: {topic}"

# Generate blog
def generate_blog(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list):
            return result[0]["generated_text"]
        elif "generated_text" in result:
            return result["generated_text"]
        else:
            return "No text generated."
    else:
        return f"Error {response.status_code}: {response.text}"

# Send email
def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("Blog sent successfully via email.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Run
print("Generating blog...")
blog = generate_blog(prompt)
print("Blog generated. Sending now...\n")
print(blog)
send_email(f"New Blog: {topic}", blog)
