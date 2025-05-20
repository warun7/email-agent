GENERIC_WORDS = {"inbox", "email", "emails", "mail", "mails", "message", "messages"}

def clean_keywords(keywords):
    """Remove generic words from the list of keywords."""
    return [kw for kw in keywords if kw.lower() not in GENERIC_WORDS]

def build_gmail_query(keywords):
    """Build a Gmail search query using OR logic for the keywords."""
    if not keywords:
        return ""
    if len(keywords) == 1:
        return keywords[0]
    # Quote multi-word keywords
    quoted = [f'"{kw}"' if " " in kw else kw for kw in keywords]
    return " OR ".join(quoted)