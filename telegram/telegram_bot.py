import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yaml
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from collections import deque

from llm.gemini_client import GeminiClient
from email_client.fetcher import GmailFetcher
from search.searcher import clean_keywords, build_gmail_query
from summarizer.summarizer import summarize_with_llm

# Load config
with open(os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml"), "r") as f:
    config = yaml.safe_load(f)
TELEGRAM_TOKEN = config.get("telegram", {}).get("token", "YOUR_TELEGRAM_BOT_TOKEN")

gemini = GeminiClient()
gmail = GmailFetcher()

# Maintain a context window for the current session only
context_window = deque(maxlen=10)
# Track the last set of relevant emails for follow-up context
last_relevant_emails = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Ask me anything about your emails.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_relevant_emails
    user_question = update.message.text
    context_window.append({"role": "user", "content": user_question})

    loading_message = await update.message.reply_text("Processing your request...")
    keywords = gemini.extract_keywords(user_question)
    filtered_keywords = clean_keywords(keywords)
    query = build_gmail_query(filtered_keywords)
    emails = gmail.search_emails([query]) if query else []

    # If the query is ambiguous (e.g., 'these', 'them', etc.), use last_relevant_emails
    ambiguous_words = ["these", "them", "those", "that", "such emails", "above", "mentioned"]
    if any(word in user_question.lower() for word in ambiguous_words) and last_relevant_emails:
        emails = last_relevant_emails

    if emails:
        last_relevant_emails = emails  # Update the last relevant emails
    else:
        await loading_message.edit_text("No emails found related to your question.")
        return

    # Build context for the LLM
    history_text = ""
    for turn in context_window:
        if turn["role"] == "user":
            history_text += f"User: {turn['content']}\n"
        elif turn["role"] == "assistant":
            history_text += f"Assistant: {turn['content']}\n"

    # Pass both history and the emails to the LLM
    summary = summarize_with_llm(gemini, f"{history_text}\nCurrent question: {user_question}", emails)
    summary = summary.replace('*', '')
    context_window.append({"role": "assistant", "content": summary})

    await loading_message.edit_text(summary)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()