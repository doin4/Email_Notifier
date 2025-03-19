# Email_Notifier

`Email_Notifier` is a Python-based template designed to monitor specific events or data and send email notifications to users. 

This template is highly customizable and can be easily adapted to monitor other types of data or events, making it a versatile starting point for building email-based notification systems.

---

## Features

- Monitor GitHub users for newly created repositories.
- Send email notifications with details, including clickable repository links.
- Easy configuration using environment variables (`.env` file).
- Modular and well-structured code for easy adaptation to other use cases.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/doin4/Email_Notifier.git
   cd Email_Notifier
   ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure the .env file with your settings:
    ```md
    USER_LIST=target,uer,name,no,space
    # You can run the script without your token
    GITHUB_TOKEN=your_personal_access_token
    EMAIL_SENDER=your_email@qq.com
    EMAIL_PASSWORD=your_email_password
    EMAIL_RECEIVER=receiver_email@example.com
    # Change the server and port accroding to your sender email
    SMTP_SERVER=smtp.qq.com
    SMTP_PORT=465
    TRACKED_REPOS_FILE=/path/to/your/own/save
    ```

4. Run the script manually:
    ```bash
    python main.py
    ```
    Note: Accroding to my test, the following error does not indicate error in sending email.
    ```bash
    Error sending email: (-1, b'\x00\x00\x00')
    ```

5. (Optional) Schedule automatic monitoring:

- Linux/Mac: Use `cron` or `crontab` to schedule the script to run periodically.
- Windows: Use Windows Task Scheduler to schedule the script.
---

## How It Works

1. **Setup**: Configure the `.env` file with GitHub usernames, email credentials, and other required settings.
2. **Monitoring**: The script fetches the list of repositories for specified GitHub users using the GitHub API.
3. **Detection**: It compares the current repository list with previously tracked repositories stored in a JSON file.
4. **Notification**: If new repositories are detected, an email notification is sent to the configured recipient.

---

## Example Use Case

This template is designed for monitoring GitHub repositories, but you can easily adapt it to monitor other types of data or events. For example:

### Current Use Case: Monitoring GitHub Repositories

The script fetches the list of repositories for specific GitHub users and detects new repositories. When a new repository is detected, it sends an email notification.

### Custom Use Case: Monitoring Weather Conditions

To modify this template to monitor weather conditions:
1. Replace the GitHub API logic (`fetch_user_repos`) with a weather API (e.g., OpenWeather API) to fetch weather data.
2. Update the logic in `check_new_repos` to monitor for specific weather conditions (e.g., rain, snow).
3. Update the email body to include the relevant weather information.
