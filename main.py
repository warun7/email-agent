import sys
import os

from llm.gemini_client import GeminiClient
from email_client.fetcher import GmailFetcher
from search.searcher import clean_keywords, build_gmail_query
from summarizer.summarizer import summarize_with_llm

# Terminal color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    gemini = GeminiClient()
    gmail = GmailFetcher()

    print(f"{Colors.HEADER}{Colors.BOLD}AI Email Assistant{Colors.ENDC}")
    user_question = input(f"{Colors.OKBLUE}Ask a question about your emails: {Colors.ENDC}")

    # Step 1: Extract keywords
    keywords = gemini.extract_keywords(user_question)
    print(f"{Colors.OKCYAN}Extracted keywords:{Colors.ENDC} {keywords}")

    # Step 2: Clean and build search query
    filtered_keywords = clean_keywords(keywords)
    query = build_gmail_query(filtered_keywords)
    print(f"{Colors.OKCYAN}Using Gmail search query:{Colors.ENDC} {query}")

    # Step 3: Search emails
    emails = gmail.search_emails([query]) if query else []
    if not emails:
        print(f"{Colors.WARNING}No emails found related to your question.{Colors.ENDC}")
        return

    # Step 4: Summarize emails
    print(f"\n{Colors.BOLD}Summary:{Colors.ENDC}")
    summary = summarize_with_llm(gemini, user_question, emails)
    print(f"{Colors.OKGREEN}{summary}{Colors.ENDC}")

if __name__ == "__main__":
    main()