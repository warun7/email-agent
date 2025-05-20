import yaml
import google.generativeai as genai

class GeminiClient:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        api_key = config['gemini']['api_key']
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemma-3-27b-it')

    def extract_keywords(self, question):
        prompt = (
            "Extract the most relevant keywords or search terms from the following question to search for in a users mail inbox. "
            "Return them as a comma-separated list, no explanations.\n"
            f"Question: {question}"
        )
        response = self.model.generate_content(prompt)
        return [keyword.strip() for keyword in response.text.split(",")]

    def summarize_emails(self, question, emails):
        # emails: list of dicts with 'subject', 'snippet', 'timestamp'
        email_texts = "\n\n".join(
            f"Subject: {email['subject']}\nSnippet: {email['snippet']}\nDate: {email['timestamp']}" for email in emails
        )
        prompt = (
            f"Given the following user question:\n{question}\n\n"
            f"And these related emails:\n{email_texts}\n\n"
            "Summarize the relevant information to answer the user's question."
        )
        response = self.model.generate_content(prompt)
        return response.text