import os
import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
USER_LIST = [user.strip() for user in os.getenv("USER_LIST", "").split(",")]  # List of users to monitor
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub Personal Access Token
EMAIL_SENDER = os.getenv("EMAIL_SENDER")  # Sender email address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Email password or authorization code
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")  # Receiver email address
SMTP_SERVER = os.getenv("SMTP_SERVER")  # SMTP server address
SMTP_PORT = int(os.getenv("SMTP_PORT"))  # SMTP server port
TRACKED_REPOS_FILE = os.getenv("TRACKED_REPOS_FILE") # File to store tracked repositories

# GitHub API headers with authentication
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}" if GITHUB_TOKEN else None
}


def fetch_user_repos(username):
    """
    Fetch all public repositories of a given GitHub user.
    :param username: GitHub username
    :return: List of repository names
    """
    url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        repos = response.json()
        return [repo["name"] for repo in repos]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories for {username}: {e}")
        return []


def load_tracked_repos():
    """
    Load the list of tracked repositories from a JSON file.
    :return: Dictionary of tracked repositories
    """
    if os.path.exists(TRACKED_REPOS_FILE):
        with open(TRACKED_REPOS_FILE, "r") as file:
            return json.load(file)
    return {}


def save_tracked_repos(tracked_repos):
    """
    Save the updated list of tracked repositories to a JSON file.
    :param tracked_repos: Dictionary of tracked repositories
    """
    with open(TRACKED_REPOS_FILE, "w") as file:
        json.dump(tracked_repos, file, indent=4)


def send_email(subject, body):
    """
    Send an email using SMTP.
    :param subject: Email subject
    :param body: Email body
    """
    try:
        # Configure email content
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to SMTP server and send the email
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def check_new_repos():
    """
    Check for new repositories for each user in the USER_LIST.
    If new repositories are found, send a notification email.
    """
    # Load previously tracked repositories
    tracked_repos = load_tracked_repos()
    new_repos_summary = {}

    for user in USER_LIST:
        print(f"Checking repositories for user: {user}")
        current_repos = fetch_user_repos(user)

        # Initialize user's repository list if not already tracked
        if user not in tracked_repos:
            tracked_repos[user] = []

        # Identify new repositories
        new_repos = [repo for repo in current_repos if repo not in tracked_repos[user]]
        if new_repos:
            new_repos_summary[user] = new_repos
            # Update the tracked repositories with the new ones
            tracked_repos[user].extend(new_repos)

    # Save the updated tracked repositories
    save_tracked_repos(tracked_repos)

    # Send email notification if there are new repositories
    if new_repos_summary:
        generate_and_send_notification(new_repos_summary)


def generate_and_send_notification(new_repos_summary):
    """
    Generate and send an email notification for new repositories.
    :param new_repos_summary: Dictionary of new repositories by user
    """
    subject = "GitHub New Repository Notification"
    body = "The following new repositories have been created:\n\n"

    # Build email body
    for user, repos in new_repos_summary.items():
        body += f"User {user} has created the following repositories:\n"
        for repo in repos:
            repo_url = f"https://github.com/{user}/{repo}"
            body += f"- {repo} ({repo_url})\n"
        body += "\n"

    # Send the email
    send_email(subject, body)


# Entry point
if __name__ == "__main__":
    check_new_repos()