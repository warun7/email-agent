# AI Email Assistant

## Overview

This project is an AI-powered email assistant that connects to your Gmail inbox and answers your questions about your emails using Google Gemini LLM. You can interact with the assistant via the command line or through a Telegram bot. The assistant can:

- Understand natural language questions about your emails
- Search your Gmail inbox for relevant emails
- Summarize and answer your questions using Gemini LLM
- Maintain conversational context for follow-up questions (in the same session)

**Note:** All email access is performed using the Gmail account configured during setup. The Telegram bot will answer using this account's inbox.

---
![image](https://github.com/user-attachments/assets/4e33695e-95d1-4593-b23f-eba5b5a2865f)

## Features

- Natural language Q&A about your Gmail inbox
- Summarization of multiple emails
- Context window for follow-up questions
- Telegram bot integration for remote access
- Colorful and user-friendly CLI output

---

## Prerequisites

- Python 3.9+
- A Google Cloud project with Gmail API enabled
- Gemini API key from Google AI Studio
- Telegram account and a Telegram bot token

---

## Setup Instructions

### 1. Clone the Repository

```sh
# Clone this repo and enter the directory
$ git clone <your-repo-url>
$ cd <repo-directory>
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Gmail API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create/select a project.
3. Enable the Gmail API.
4. Configure the OAuth consent screen (External, add your email as a test user).
5. Create OAuth credentials (Desktop app) and download `credentials.json`.
6. Place the credentials file in the `config/` folder and update `config.yaml`:
   ```yaml
   gmail:
   credentials_file: "config/credentials.json"
   token_file: "config/token.json"
   ```
7. The first time you run the assistant, it will prompt you to authenticate and create `token.json`.

### 4. Gemini API Setup

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Create an API key and add it to `config/config.yaml`:
   ```yaml
   gemini:
   api_key: "YOUR_GEMINI_API_KEY"
   ```

### 5. Telegram Bot Setup (Optional)

1. Talk to [@BotFather](https://t.me/botfather) on Telegram.
2. Create a new bot and get the token.
3. Add the token to `config/config.yaml`:
   ```yaml
   telegram:
   token: "YOUR_TELEGRAM_BOT_TOKEN"
   ```

---

## Running the Assistant

### **Command Line Interface (CLI)**

```sh
python main.py
```

- Ask questions about your emails directly in the terminal.

### **Telegram Bot**

```sh
python telegram/telegram_bot.py
```

- Interact with your assistant from anywhere via Telegram.
- The bot will respond to your questions and maintain context for follow-ups during the session.

---

## Project Structure

```
email_assistant/
├── config/                # Configuration files (API keys, settings)
├── data/                  # Local data or cache
├── email_client/          # Gmail connection and fetching
├── llm/                   # Gemini LLM interaction
├── search/                # Email search/filter logic
├── summarizer/            # Summarization logic
├── telegram/              # Telegram bot integration
├── main.py                # CLI entry point
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## Security & Privacy

- All email access is performed using the Gmail account you authenticate during setup.
- The Telegram bot will answer using this account's inbox for all users.
- **Do not share your credentials or tokens.**

---
