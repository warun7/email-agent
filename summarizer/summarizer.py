def summarize_with_llm(gemini_client, question, emails):
    """
    Summarize emails using Gemini.
    gemini_client: instance of GeminiClient
    question: str
    emails: list of dicts with 'subject', 'snippet', 'timestamp'
    """
    if not emails:
        return "No emails found related to your question."
    return gemini_client.summarize_emails(question, emails)