import os
import yaml
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime

class GmailFetcher:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.credentials_file = config['gmail']['credentials_file']
        self.token_file = config['gmail']['token_file']
        self.max_results = config.get('search', {}).get('max_results', 20)
        self.service = self.authenticate()

    def authenticate(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def search_emails(self, keywords):
        # Build Gmail search query
        query = " ".join(keywords)
        results = self.service.users().messages().list(
            userId='me', q=query, maxResults=self.max_results
        ).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            msg_data = self.service.users().messages().get(
                userId='me', id=msg['id'], format='metadata', metadataHeaders=['Subject', 'Date']
            ).execute()
            headers = msg_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            snippet = msg_data.get('snippet', '')
            # Convert date to readable format
            try:
                timestamp = datetime.strptime(date[:-6], "%a, %d %b %Y %H:%M:%S")
            except Exception:
                timestamp = date
            emails.append({'subject': subject, 'snippet': snippet, 'timestamp': str(timestamp)})
        return emails