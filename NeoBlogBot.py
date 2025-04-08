import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from random import choice

# Load environment variables (from GitHub Secrets)
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
app_password = os.getenv("APP_PASSWORD")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

print("Loaded secrets:")
print(f"SENDER: {sender_email}")
print(f"RECEIVER: {receiver_email}")

# Hugging Face API setup
model = "mistralai/Mistral-7B-Instruct-v0.1"
api_url = f"https://api-inference.huggingface.co/models/{model}"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

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

# Choose random topic
topic = choice(topics)
prompt = f"Write a creative, human-like blog post on the topic: {topic}"

def generate_blog(prompt):
    print(f"Generating blog on: {topic}")
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500, "temperature": 0.7, "top_p": 0.9}
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        print("Blog generated successfully.")
        if isinstance(result, list):
            return result[0]["generated_text"]
        elif "generated_text" in result:
            return result["generated_text"]
    print(f"Failed to generate blog: {response.status_code}, {response.text}")
    return f"ERROR: {response.status_code} - {response.text}"

# Send email
def send_email(subject, body):
    print("Preparing to send email...")
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Run
blog_text = generate_blog(prompt)

# Save the blog
filename = f"blog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(filename, "w") as f:
    f.write(blog_text)
print(f"Saved blog to {filename}")

# Email the blog
send_email(f"NeoBlog: {topic}", blog_text)
